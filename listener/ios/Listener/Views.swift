import MapKit
import PhotosUI
import SwiftData
import SwiftUI

struct RootView: View {
    @Environment(\.modelContext) private var context
    @Query(filter: #Predicate<Session> { $0.status == "active" }) private var sessions: [Session]
    @StateObject private var location = LocationService()
    @StateObject private var audio = AudioService()
    @StateObject private var sync = SyncQueue()
    @State private var tab = 0
    @State private var showInstrument = false

    var session: Session? { sessions.first }

    var body: some View {
        ZStack {
            Color(red: 0.008, green: 0.02, blue: 0.016).ignoresSafeArea()
            if !showInstrument || session == nil {
                RecordHomeView(location: location, audio: audio, sync: sync) {
                    showInstrument = true
                }
            } else {
                VStack(spacing: 0) {
                    header
                    Picker("", selection: $tab) {
                        Text("FIELD").tag(0)
                        Text("BROADCAST").tag(1)
                        Text("SIGNALS").tag(2)
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal)
                    Group {
                        if tab == 0 {
                            FieldView(session: session!, location: location, audio: audio, sync: sync)
                        } else if tab == 1 {
                            BroadcastView(session: session!)
                        } else {
                            LibraryView(session: session!)
                        }
                    }
                }
            }
        }
        .preferredColorScheme(.dark)
        .onAppear { location.ask() }
    }

    private var header: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text("LISTENER").font(.caption.weight(.black)).tracking(4)
                Text("WHAT THE WILD IS SAYING").font(.system(size: 8)).foregroundStyle(Color(red: 0.57, green: 0.64, blue: 0.60))
            }
            Spacer()
            VStack(alignment: .trailing) {
                Text(location.quality == "fading" ? "● GPS FADING" : "● FIELD READY")
                    .font(.system(size: 9)).foregroundStyle(Color(red: 0.49, green: 1.0, blue: 0.65))
                Text(session == nil ? "NO SESSION" : "1 LISTENER").font(.system(size: 9))
            }
        }
        .padding()
    }
}

struct RecordHomeView: View {
    @Environment(\.modelContext) private var context
    @Query(filter: #Predicate<Session> { $0.status == "active" }) private var sessions: [Session]
    @Query private var encounters: [Encounter]
    @ObservedObject var location: LocationService
    @ObservedObject var audio: AudioService
    @ObservedObject var sync: SyncQueue
    var openInstrument: () -> Void
    @State private var micDenied = false
    @State private var saved = false
    @State private var airPulse = true

    var session: Session? { sessions.first }

    var body: some View {
        VStack(spacing: 28) {
            Text("LISTENER").tracking(6).font(.caption.weight(.black))
            Text(statusLine)
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
                .padding(.horizontal, 28)
            if audio.recording {
                HStack(spacing: 10) {
                    Circle().fill(Color.red).frame(width: 16, height: 16).opacity(0.2)
                        .overlay(Circle().fill(Color.red).frame(width: 16, height: 16).opacity(airPulse ? 1 : 0.15))
                    Text("ON AIR").font(.title2.weight(.black)).tracking(4).foregroundStyle(.red)
                }
            }
            Spacer()
            Button(audio.recording ? ListenerCopy.stop : ListenerCopy.start) {
                if audio.recording { stopRecord() } else { startRecord() }
            }
            .frame(width: 260, height: 260)
            .background(audio.recording ? Color(red: 0.36, green: 0.12, blue: 0.14) : Color(red: 0.12, green: 0.36, blue: 0.24))
            .foregroundStyle(.white)
            .font(.system(size: 52, weight: .black))
            .clipShape(Circle())
            .shadow(color: audio.recording ? Color.red.opacity(0.45) : Color.green.opacity(0.45), radius: 28)
            Spacer()
            Button("Field instrument") {
                if session == nil { ensureSession() }
                openInstrument()
            }
            .font(.footnote)
            .foregroundStyle(.secondary)
        }
        .padding(28)
        .onChange(of: audio.recording) { _, on in
            if on { airPulse.toggle() }
        }
    }

    private var statusLine: String {
        if audio.recording { return "Recording. Original stays on this phone." }
        if micDenied { return ListenerCopy.micDenied }
        if saved || encounters.contains(where: { $0.sessionId == session?.id }) {
            return "Saved on this phone. Not sent anywhere. UNKNOWN stays UNKNOWN."
        }
        return "Tap START. Put the phone down. Tap STOP when you are done."
    }

    private func ensureSession() {
        if session != nil { return }
        let next = Session(door: .listen, role: .base)
        if let loc = location.last {
            next.startLat = loc.coordinate.latitude
            next.startLon = loc.coordinate.longitude
            next.startAccuracy = loc.horizontalAccuracy
            next.startGpsQuality = location.quality
        }
        context.insert(next)
        context.insert(FieldNode(sessionId: next.id, role: .base, name: "BASE · YOU", coordinate: next.startCoordinate))
        sync.enqueue(context: context, type: "session.open", payload: [
            "sessionId": next.id.uuidString,
            "invite": next.inviteCode,
        ])
        try? context.save()
    }

    private func startRecord() {
        ensureSession()
        do {
            try audio.start()
            micDenied = false
        } catch {
            micDenied = true
        }
    }

    private func stopRecord() {
        let url = audio.recording ? audio.stop() : audio.lastOriginalURL
        guard let current = (try? context.fetch(FetchDescriptor<Session>()))?.first(where: { $0.status == "active" }) else { return }
        let note = FieldNote(
            sessionId: current.id,
            kind: .heard,
            text: "",
            mediaPath: url?.path,
            coordinate: location.last?.coordinate ?? current.startCoordinate
        )
        context.insert(note)
        let enc = Encounter(sessionId: current.id, label: "UNKNOWN", kind: .unknown)
        enc.lat = note.lat
        enc.lon = note.lon
        enc.originalAudioPath = url?.path
        enc.contributed = false
        enc.shared = false
        context.insert(enc)
        sync.enqueue(context: context, type: "note.add", payload: [
            "note": note.id.uuidString,
            "firstSound": "true",
        ])
        try? context.save()
        saved = true
    }
}

struct FieldView: View {
    @Environment(\.modelContext) private var context
    @Bindable var session: Session
    @ObservedObject var location: LocationService
    @ObservedObject var audio: AudioService
    @ObservedObject var sync: SyncQueue
    @Query private var crumbs: [Breadcrumb]
    @Query private var notes: [FieldNote]
    @Query private var encounters: [Encounter]
    @State private var noteOpen = false
    @State private var scoutOpen = false
    @State private var firstSoundOpen = false

    var body: some View {
        ZStack {
            map
            VStack {
                HStack {
                    VStack(alignment: .leading) {
                        Text("FIELD COHERENCE · DA").font(.system(size: 8)).foregroundStyle(.secondary)
                        Text(CohResult.insufficient.display).font(.title)
                        Text(CohResult.insufficient.status).font(.system(size: 8)).foregroundStyle(Color(red: 0.49, green: 1, blue: 0.65))
                    }
                    .padding(10)
                    .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
                    Spacer()
                    Text("N\n↑").multilineTextAlignment(.center)
                        .frame(width: 70, height: 70)
                        .background(.ultraThinMaterial, in: Circle())
                        .rotationEffect(.degrees(location.heading?.trueHeading ?? 0))
                }
                .padding()
                Spacer()
                Text(audio.recording ? "MIC · \(audio.activeInput.uppercased()) · RECORDING · ORIGINAL PRESERVED" : "MIC · \(audio.activeInput.uppercased()) · IDLE")
                    .font(.system(size: 8))
                    .foregroundStyle(audio.recording ? Color(red: 0.49, green: 1, blue: 0.65) : .secondary)
                liveCard
                HStack {
                    Button("＋ SESSION") { }
                    Button("FIELD NOTE") { noteOpen = true }
                    Button("↶ RETURN") { session.returnActive.toggle() }
                    Button("GO SCOUT") { scoutOpen = true; session.role = Role.scout.rawValue }
                }
                .font(.system(size: 10))
                .padding(8)
                .background(.ultraThinMaterial, in: Capsule())
                .padding(.bottom, 12)
            }
        }
        .sheet(isPresented: $noteOpen) { NoteSheet(session: session, location: location, audio: audio, sync: sync) }
        .sheet(isPresented: $scoutOpen) { ScoutSheet(session: session, audio: audio) }
        .sheet(isPresented: $firstSoundOpen) { FirstSoundSheet(session: session, location: location, audio: audio, sync: sync) }
        .onAppear {
            // Field instrument is opt-in. Do not auto-open a first-sound sheet.
        }
        .onChange(of: location.last) { _, loc in
            guard session.role == Role.scout.rawValue, let loc else { return }
            context.insert(Breadcrumb(sessionId: session.id, loc: loc))
            try? context.save()
        }
    }

    private var map: some View {
        Map {
            if let start = session.startCoordinate {
                Marker("START", coordinate: start)
            }
            if let you = location.last?.coordinate {
                Marker(session.role == Role.base.rawValue ? "BASE · YOU" : "SCOUT · YOU", coordinate: you)
            }
            ForEach(crumbs.filter { $0.sessionId == session.id }, id: \.id) { crumb in
                if session.returnActive {
                    Marker("", coordinate: crumb.coordinate)
                }
            }
            let coords = crumbs.filter { $0.sessionId == session.id }.map(\.coordinate)
            if coords.count > 1 {
                MapPolyline(coordinates: coords).stroke(Color(red: 0.49, green: 1, blue: 0.65), lineWidth: 3)
            }
            ForEach(notes.filter { $0.sessionId == session.id && $0.lat != nil }, id: \.id) { note in
                Marker(note.kind.uppercased(), coordinate: CLLocationCoordinate2D(latitude: note.lat!, longitude: note.lon!))
            }
        }
        .mapStyle(mapStyle)
        .safeAreaInset(edge: .top) {
            Picker("Map", selection: $session.mapMode) {
                Text("FIELD").tag(MapMode.field.rawValue)
                Text("SAT").tag(MapMode.satellite.rawValue)
                Text("HYBRID").tag(MapMode.hybrid.rawValue)
            }
            .pickerStyle(.segmented)
            .padding(.horizontal, 80)
        }
        .ignoresSafeArea()
    }

    private var mapStyle: MapStyle {
        switch session.mapMode {
        case MapMode.satellite.rawValue: return .imagery
        case MapMode.hybrid.rawValue: return .hybrid
        default: return .standard(elevation: .realistic, pointsOfInterest: .excludingAll)
        }
    }

    private var liveCard: some View {
        let last = encounters.filter { $0.sessionId == session.id && !$0.excluded }.last
        let first = last != nil && encounters.filter { $0.sessionId == session.id && !$0.excluded }.count == 1
        return Button {
            if last == nil { firstSoundOpen = true }
        } label: {
            HStack {
                VStack(alignment: .leading) {
                    Text(last == nil ? ListenerCopy.firstSound : (first ? "FIRST SOUND · ON THIS PHONE" : "FIELD NOTE · NON-HUMAN"))
                        .font(.system(size: 8)).foregroundStyle(.secondary)
                    Text(last?.label ?? ListenerCopy.listenRain).font(.subheadline.bold())
                    Text(last == nil ? "Original stays on this phone. Not contributed." : (first ? ListenerCopy.firstSoundKept : ListenerCopy.sharingIsNotContributing))
                        .font(.system(size: 10)).foregroundStyle(.secondary)
                }
                Spacer()
                Text(last == nil ? "TAP TO\nLISTEN" : (last?.contributed == true ? "IN LIBRARY" : "NOT\nCONTRIBUTED"))
                    .font(.system(size: 8)).foregroundStyle(Color(red: 0.49, green: 1, blue: 0.65))
            }
            .padding()
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 17))
            .padding(.horizontal)
        }
        .buttonStyle(.plain)
    }
}

struct FirstSoundSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var context
    @Bindable var session: Session
    @ObservedObject var location: LocationService
    @ObservedObject var audio: AudioService
    @ObservedObject var sync: SyncQueue
    @State private var kind = NoteKind.heard
    @State private var text = ""
    @State private var micDenied = false

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("FIRST SOUND · ON THIS PHONE").font(.caption)
            Text(micDenied ? "Microphone is off" : "Listening to this rain").font(.title)
            Text(micDenied ? ListenerCopy.micDenied : "The original is being kept. This is not a species and it is not contributed.")
                .foregroundStyle(.secondary)
            if micDenied {
                Button("TRY THE MICROPHONE AGAIN") { arm() }.buttonStyle(WideButton())
            }
            HStack {
                Button("👂 HEARD") { kind = .heard }
                Button("❓ MYSTERY") { kind = .mystery }
            }
            TextField("Your words — rain, or leave UNKNOWN.", text: $text, axis: .vertical)
            Button(micDenied ? "KEEP A FIELD NOTE" : "STOP AND KEEP") { save() }.buttonStyle(WideButton())
            Button("KEEP THE SESSION") { dismiss() }
        }
        .padding()
        .onAppear { arm() }
    }

    private func arm() {
        do {
            try audio.start()
            micDenied = false
        } catch {
            micDenied = true
        }
    }

    private func save() {
        let url = audio.recording ? audio.stop() : audio.lastOriginalURL
        let words = text.trimmingCharacters(in: .whitespacesAndNewlines)
        let label = words.isEmpty ? "UNKNOWN" : words
        let note = FieldNote(
            sessionId: session.id,
            kind: kind,
            text: words,
            mediaPath: url?.path,
            coordinate: location.last?.coordinate ?? session.startCoordinate
        )
        context.insert(note)
        let enc = Encounter(sessionId: session.id, label: label, kind: .unknown)
        enc.lat = note.lat
        enc.lon = note.lon
        enc.originalAudioPath = url?.path
        enc.contributed = false
        enc.shared = false
        context.insert(enc)
        sync.enqueue(context: context, type: "note.add", payload: [
            "note": note.id.uuidString,
            "firstSound": "true",
        ])
        try? context.save()
        dismiss()
    }
}

struct ScoutSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Bindable var session: Session
    @ObservedObject var audio: AudioService

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("STUPIDLY EASY SETUP").font(.caption)
            Text("Go Scout").font(.title)
            Text("Take this phone. Listener checks location, microphone and connected AirPods, starts your breadcrumb trail and links to a Base when one is there.")
                .foregroundStyle(.secondary)
            Text("Active input · \(audio.activeInput)")
            Button("START WANDER") {
                session.role = Role.scout.rawValue
                audio.refreshInput()
                try? audio.start()
                dismiss()
            }
            .buttonStyle(WideButton())
        }
        .padding()
        .onAppear { audio.refreshInput() }
    }
}

struct NoteSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var context
    @Bindable var session: Session
    @ObservedObject var location: LocationService
    @ObservedObject var audio: AudioService
    @ObservedObject var sync: SyncQueue
    @State private var kind = NoteKind.mystery
    @State private var text = ""
    @State private var photo: PhotosPickerItem?

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("FIELD NOTE · AUTO-STAMPED").font(.caption)
            Text("What happened?").font(.title)
            LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())]) {
                Button("👁 SAW IT") { kind = .saw }
                Button("👂 HEARD IT") { kind = .heard }
                PhotosPicker("📷 PHOTO", selection: $photo, matching: .images)
                PhotosPicker("🎞 VIDEO", selection: $photo, matching: .videos)
                Button("❓ MYSTERY") { kind = .mystery }
                Button("🗣 HUMAN SPEECH") { kind = .heard; save(human: true) }
            }
            TextField("Optional words from you — never a transcript of the recording.", text: $text, axis: .vertical)
            Button("SAVE EVIDENCE") { save(human: false) }.buttonStyle(WideButton())
        }
        .padding()
    }

    private func save(human: Bool) {
        var mediaPath: String?
        if let url = audio.lastOriginalURL, kind == .heard {
            mediaPath = url.path
        }
        let note = FieldNote(
            sessionId: session.id,
            kind: kind,
            text: text,
            mediaPath: mediaPath,
            coordinate: location.last?.coordinate ?? session.startCoordinate
        )
        context.insert(note)
        if human {
            // Probable human speech: keep an internal exclusion only. No wildlife encounter.
            try? context.save()
            dismiss()
            return
        }
        let enc = Encounter(sessionId: session.id, label: kind == .mystery ? "UNKNOWN" : (text.isEmpty ? kind.rawValue.uppercased() : text))
        enc.lat = note.lat
        enc.lon = note.lon
        enc.originalAudioPath = mediaPath
        context.insert(enc)
        sync.enqueue(context: context, type: "note.add", payload: ["note": note.id.uuidString])
        try? context.save()
        dismiss()
    }
}

struct LibraryView: View {
    @Environment(\.modelContext) private var context
    var session: Session
    @Query private var library: [LibraryContribution]
    @Query private var encounters: [Encounter]
    @State private var selected: Encounter?
    @State private var confirmed = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                Text("LISTENER SIGNAL LIBRARY").font(.title)
                Text("Contributed non-human signals only · provenance never silently merged")
                    .font(.caption).foregroundStyle(.secondary)
                if library.isEmpty {
                    labeled("Nothing contributed yet", sub: ListenerCopy.sharingIsNotContributing)
                }
                ForEach(library, id: \.id) { row in
                    labeled(row.label, sub: "\(row.provenance) · coarse \(row.coarseLat.map(String.init) ?? "held")")
                }
                Text("Human-speech exclusion before any common-library upload.").font(.caption)
                ForEach(encounters.filter { $0.sessionId == session.id && !$0.excluded }, id: \.id) { enc in
                    Button(enc.label) { selected = enc }
                }
                Button("THIS IS NOT HUMAN SPEECH") {
                    if let selected { _ = selected.confirmNonHuman(); confirmed = true }
                }
                Button("SEND US YOUR LISTENER SIGNALS") {
                    guard let selected, selected.canContribute() == nil else { return }
                    let row = LibraryContribution(from: selected, includeAudio: selected.originalAudioPath != nil)
                    selected.contributed = true
                    context.insert(row)
                    try? context.save()
                }
                .buttonStyle(WideButton())
                Button("SHARE A CARD ONLY") {
                    guard let selected else { return }
                    selected.shared = true
                    context.insert(ListenerCard(encounterId: selected.id))
                    try? context.save()
                }
            }
            .padding()
        }
    }

    private func labeled(_ title: String, sub: String) -> some View {
        VStack(alignment: .leading) {
            Text(title).bold()
            Text(sub).font(.caption).foregroundStyle(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(red: 0.03, green: 0.06, blue: 0.05), in: RoundedRectangle(cornerRadius: 16))
    }
}

struct BroadcastView: View {
    var session: Session
    @Query private var rooms: [BroadcastRoom]

    var body: some View {
        let room = rooms.first { $0.sessionId == session.id }
        VStack(alignment: .leading, spacing: 14) {
            Text(room == nil ? "○ BROADCAST READY" : "● LIVE BROADCAST").foregroundStyle(.red)
            Text(room?.title ?? "No broadcast yet").font(.largeTitle)
            Text("People join the party. Listener nodes join the field. Watching is not contributing.")
                .foregroundStyle(.secondary)
            labeled("\(room?.watchers ?? 0) watching", sub: "Watching needs no microphone and no precise location.")
            labeled("Invite \(session.inviteCode)", sub: "Pair another Listener. Transport is replaceable. Offline keeps the Session.")
        }
        .padding()
    }

    private func labeled(_ title: String, sub: String) -> some View {
        VStack(alignment: .leading) {
            Text(title).bold()
            Text(sub).font(.caption).foregroundStyle(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(red: 0.03, green: 0.06, blue: 0.05), in: RoundedRectangle(cornerRadius: 16))
    }
}

struct WideButton: ButtonStyle {
    var alt = false
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity)
            .padding()
            .background(alt ? Color(red: 0.05, green: 0.10, blue: 0.08) : Color(red: 0.09, green: 0.22, blue: 0.16))
            .foregroundStyle(.white)
            .clipShape(RoundedRectangle(cornerRadius: 14))
    }
}
