import CoreLocation
import Foundation
import SwiftData

enum Door: String, Codable { case listen, scout, broadcast }
enum Role: String, Codable { case hub, base, scout, node }
enum MapMode: String, Codable { case field, satellite, hybrid }
enum NoteKind: String, Codable { case saw, heard, photo, video, mystery }
enum EncounterKind: String, Codable { case unknown, wildlife, probableHumanExcluded }
enum Provenance: String, Codable {
    case listenerMeasurement, user, classifier, reference, expertValidation
}
enum SpeechGate: String, Codable { case pending, excluded, excludedAsHuman }

enum ListenerCopy {
    static let product = "What the wild is saying."
    static let scoutLost = "Scout connection lost. Still recording — we'll sync when you're back."
    static let cohMark = "—"
    static let cohStatus = "INSUFFICIENT FIELD DATA"
    static let leaveAsBase = "Another Listener is available. LEAVE AS BASE?"
    static let sharingIsNotContributing = "Sharing a card is not contributing the original."
    static let firstSound = "THIS IS THE FIRST SOUND"
    static let listenRain = "LISTEN TO THIS RAIN"
    static let start = "START"
    static let stop = "STOP"
    static let micDenied = "This phone needs the microphone to keep the original. Your session is still here."
    static let firstSoundKept = "The first sound is on this phone. Original preserved. Not contributed."
}

@Model
final class Session {
    @Attribute(.unique) var id: UUID
    var startedAt: Date
    var door: String
    var role: String
    var inviteCode: String
    var startLat: Double?
    var startLon: Double?
    var startAccuracy: Double?
    var startGpsQuality: String
    var status: String
    var returnActive: Bool
    var mapMode: String
    var title: String
    var broadcastId: UUID?

    init(door: Door, role: Role) {
        self.id = UUID()
        self.startedAt = Date()
        self.door = door.rawValue
        self.role = role.rawValue
        self.inviteCode = Session.makeInvite()
        self.startGpsQuality = "unknown"
        self.status = "active"
        self.returnActive = false
        self.mapMode = MapMode.field.rawValue
        self.title = "Field session"
    }

    var startCoordinate: CLLocationCoordinate2D? {
        guard let startLat, let startLon else { return nil }
        return CLLocationCoordinate2D(latitude: startLat, longitude: startLon)
    }

    static func makeInvite() -> String {
        let alphabet = Array("ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
        return String((0..<6).map { _ in alphabet.randomElement()! })
    }
}

@Model
final class Breadcrumb {
    var id: UUID
    var sessionId: UUID
    var t: Date
    var lat: Double
    var lon: Double
    var accuracy: Double
    var heading: Double?
    var quality: String

    init(sessionId: UUID, loc: CLLocation) {
        self.id = UUID()
        self.sessionId = sessionId
        self.t = loc.timestamp
        self.lat = loc.coordinate.latitude
        self.lon = loc.coordinate.longitude
        self.accuracy = loc.horizontalAccuracy
        self.heading = loc.course >= 0 ? loc.course : nil
        self.quality = loc.horizontalAccuracy <= 15 ? "good" : loc.horizontalAccuracy <= 40 ? "fair" : "fading"
    }

    var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: lat, longitude: lon)
    }
}

@Model
final class FieldNode {
    var id: UUID
    var sessionId: UUID
    var role: String
    var name: String
    var lat: Double?
    var lon: Double?
    var nearby: Bool
    var synchronized: Bool
    var lastSeen: Date

    init(sessionId: UUID, role: Role, name: String, coordinate: CLLocationCoordinate2D?) {
        self.id = UUID()
        self.sessionId = sessionId
        self.role = role.rawValue
        self.name = name
        self.lat = coordinate?.latitude
        self.lon = coordinate?.longitude
        self.nearby = true
        self.synchronized = false
        self.lastSeen = Date()
    }
}

@Model
final class FieldNote {
    var id: UUID
    var sessionId: UUID
    var t: Date
    var kind: String
    var text: String
    var mediaPath: String?
    var lat: Double?
    var lon: Double?

    init(sessionId: UUID, kind: NoteKind, text: String, mediaPath: String?, coordinate: CLLocationCoordinate2D?) {
        self.id = UUID()
        self.sessionId = sessionId
        self.t = Date()
        self.kind = kind.rawValue
        self.text = text
        self.mediaPath = mediaPath
        self.lat = coordinate?.latitude
        self.lon = coordinate?.longitude
    }
}

@Model
final class Encounter {
    var id: UUID
    var sessionId: UUID
    var t: Date
    var kind: String
    var label: String
    var candidateId: String?
    var confidence: Double?
    var provenance: String
    var excluded: Bool
    var exclusionReason: String?
    var originalAudioPath: String?
    var lat: Double?
    var lon: Double?
    var humanSpeechGate: String
    var shared: Bool
    var contributed: Bool

    init(sessionId: UUID, label: String, kind: EncounterKind = .unknown) {
        self.id = UUID()
        self.sessionId = sessionId
        self.t = Date()
        self.kind = kind.rawValue
        self.label = label
        self.provenance = Provenance.user.rawValue
        self.excluded = kind == .probableHumanExcluded
        self.humanSpeechGate = SpeechGate.pending.rawValue
        self.shared = false
        self.contributed = false
    }

    func excludeAsHuman() {
        kind = EncounterKind.probableHumanExcluded.rawValue
        excluded = true
        exclusionReason = "probable_human_speech"
        humanSpeechGate = SpeechGate.excludedAsHuman.rawValue
        label = "EXCLUDED · PROBABLE HUMAN"
        candidateId = nil
        confidence = nil
    }

    func confirmNonHuman() -> String? {
        if kind == EncounterKind.probableHumanExcluded.rawValue {
            return "Already excluded as probable human speech."
        }
        humanSpeechGate = SpeechGate.excluded.rawValue
        if kind != EncounterKind.wildlife.rawValue {
            kind = EncounterKind.unknown.rawValue
        }
        return nil
    }

    func canContribute() -> String? {
        if excluded || kind == EncounterKind.probableHumanExcluded.rawValue {
            return "Probable human speech stays off the wildlife library."
        }
        if humanSpeechGate != SpeechGate.excluded.rawValue {
            return "Confirm this is not human speech before sending it to the library."
        }
        return nil
    }

    static func coarse(lat: Double?, lon: Double?) -> (Double, Double)? {
        guard let lat, let lon else { return nil }
        return ((lat * 10).rounded() / 10, (lon * 10).rounded() / 10)
    }
}

@Model
final class ListenerCard {
    var id: UUID
    var encounterId: UUID
    var shared: Bool
    var contributed: Bool

    init(encounterId: UUID) {
        self.id = UUID()
        self.encounterId = encounterId
        self.shared = true
        self.contributed = false
    }
}

@Model
final class LibraryContribution {
    var id: UUID
    var encounterId: UUID
    var label: String
    var provenance: String
    var coarseLat: Double?
    var coarseLon: Double?
    var includeAudio: Bool
    var sharedPublic: Bool
    var createdAt: Date

    init(from encounter: Encounter, includeAudio: Bool) {
        self.id = UUID()
        self.encounterId = encounter.id
        self.label = encounter.label
        self.provenance = encounter.provenance
        let coarse = Encounter.coarse(lat: encounter.lat, lon: encounter.lon)
        self.coarseLat = coarse?.0
        self.coarseLon = coarse?.1
        self.includeAudio = includeAudio
        self.sharedPublic = false
        self.createdAt = Date()
    }
}

@Model
final class BroadcastRoom {
    var id: UUID
    var sessionId: UUID
    var title: String
    var startedAt: Date
    var watchers: Int
    var sensorOptIn: Bool

    init(sessionId: UUID, title: String) {
        self.id = UUID()
        self.sessionId = sessionId
        self.title = title
        self.startedAt = Date()
        self.watchers = 1
        self.sensorOptIn = false
    }
}

@Model
final class SyncEvent {
    var id: UUID
    var t: Date
    var type: String
    var payload: Data
    var delivered: Bool

    init(type: String, payload: Data) {
        self.id = UUID()
        self.t = Date()
        self.type = type
        self.payload = payload
        self.delivered = false
    }
}

@Model
final class DevicePair {
    var id: UUID
    var role: String
    var pairedAt: Date

    init(role: Role) {
        self.id = UUID()
        self.role = role.rawValue
        self.pairedAt = Date()
    }
}

struct CohResult: Equatable {
    var display: String
    var status: String
    var computed: Bool

    static let insufficient = CohResult(
        display: ListenerCopy.cohMark,
        status: ListenerCopy.cohStatus,
        computed: false
    )

    static func from(nearbySynchronizedNodes: Int, windowSeconds: Double) -> CohResult {
        if nearbySynchronizedNodes < 2 || windowSeconds <= 0 {
            return .insufficient
        }
        return .insufficient
    }
}
