import AVFoundation
import Combine
import CoreLocation
import Foundation
import SwiftData

@MainActor
final class LocationService: NSObject, ObservableObject, CLLocationManagerDelegate {
    @Published var last: CLLocation?
    @Published var heading: CLHeading?
    @Published var quality: String = "unknown"
    @Published var denied = false

    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.activityType = .fitness
    }

    func ask() {
        manager.requestWhenInUseAuthorization()
        manager.startUpdatingLocation()
        manager.startUpdatingHeading()
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let loc = locations.last else { return }
        last = loc
        quality = loc.horizontalAccuracy <= 15 ? "good" : loc.horizontalAccuracy <= 40 ? "fair" : "fading"
    }

    func locationManager(_ manager: CLLocationManager, didUpdateHeading newHeading: CLHeading) {
        heading = newHeading
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        denied = manager.authorizationStatus == .denied
        if manager.authorizationStatus == .authorizedWhenInUse || manager.authorizationStatus == .authorizedAlways {
            manager.startUpdatingLocation()
        }
    }
}

@MainActor
final class AudioService: ObservableObject {
    @Published var activeInput = "iPhone mic"
    @Published var recording = false
    @Published var lastOriginalURL: URL?

    private var recorder: AVAudioRecorder?
    private let originals: URL

    init() {
        let dir = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("Originals", isDirectory: true)
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        originals = dir
    }

    func refreshInput() {
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.playAndRecord, mode: .measurement, options: [.allowBluetooth, .defaultToSpeaker])
        try? session.setActive(true)
        if let inputs = session.availableInputs {
            if let pods = inputs.first(where: { $0.portType == .bluetoothHFP || $0.portName.localizedCaseInsensitiveContains("AirPods") }) {
                try? session.setPreferredInput(pods)
                activeInput = pods.portName
            } else if let builtIn = inputs.first(where: { $0.portType == .builtInMic }) {
                try? session.setPreferredInput(builtIn)
                activeInput = builtIn.portName
            } else {
                activeInput = session.currentRoute.inputs.first?.portName ?? "iPhone mic"
            }
        }
    }

    func start() throws {
        refreshInput()
        let name = "listen-\(Int(Date().timeIntervalSince1970)).m4a"
        let url = originals.appendingPathComponent(name)
        let settings: [String: Any] = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 48000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue,
        ]
        recorder = try AVAudioRecorder(url: url, settings: settings)
        recorder?.record()
        recording = true
        lastOriginalURL = url
    }

    func stop() -> URL? {
        recorder?.stop()
        recording = false
        return lastOriginalURL
    }
}

protocol SyncTransport: AnyObject {
    var name: String { get }
    func send(event: SyncEvent) async throws
}

final class LocalNetworkTransport: SyncTransport {
    let name = "local-network"
    func send(event: SyncEvent) async throws {
        _ = event
    }
}

final class HubTransport: SyncTransport {
    let name = "hub"
    let baseURL: URL
    init(baseURL: URL) { self.baseURL = baseURL }

    func send(event: SyncEvent) async throws {
        var req = URLRequest(url: baseURL.appending(path: "v1/events"))
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "content-type")
        req.httpBody = event.payload
        let (_, res) = try await URLSession.shared.data(for: req)
        guard let http = res as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw NSError(domain: "listener.sync", code: 1, userInfo: [NSLocalizedDescriptionKey: ListenerCopy.scoutLost])
        }
    }
}

@MainActor
final class SyncQueue: ObservableObject {
    func enqueue(context: ModelContext, type: String, payload: [String: String]) {
        let data = (try? JSONSerialization.data(withJSONObject: payload)) ?? Data()
        context.insert(SyncEvent(type: type, payload: data))
    }

    func flush(context: ModelContext, transport: SyncTransport) async {
        let pending = (try? context.fetch(FetchDescriptor<SyncEvent>()))?.filter { !$0.delivered } ?? []
        for event in pending {
            do {
                try await transport.send(event: event)
                event.delivered = true
            } catch {
                return
            }
        }
    }
}
