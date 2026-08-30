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

    var session: Session? { sessions.first }

    var body: some View {
        ZStack {
            Color(red: 0.008, green: 0.02, blue: 0.016).ignoresSafeArea()
            if session == nil {
                OnboardingView(location: location, sync: sync)
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

struct OnboardingView: View {
    @Environment(\.modelContext) private var context
    @Query private var pairs: [DevicePair]
    @ObservedObject var location: LocationService
    @ObservedObject var sync: SyncQueue
    @State private var hello = true

    var body: some View {
        VStack(spacing: 18) {
            Text("LISTENER").tracking(6).font(.caption.weight(.black))
            if hello {
                Text(ListenerCopy.product).font(.title)
                Text("A field instrument for non-human sound. Private on this phone until you choose otherwise.")
                    .multilineTextAlignment(.center)
                    .foregroundStyle(.secondary)
                Button("CONTINUE") { hello = false }.buttonStyle(WideButton())
            } else {
                Text("How do you want to begin?").font(.title2)
                if !pairs.isEmpty {
                    Text(ListenerCopy.leaveAsBase).foregroundStyle(.secondary)
                }
                Button("LISTEN HERE") { open(.listen, role: .base) }.buttonStyle(WideButton())
                Button("GO SCOUT") { open(.scout, role: .scout) }.buttonStyle(WideButton(alt: true))
                Button("START A BROADCAST") { open(.broadcast, role: .hub) }.buttonStyle(WideButton(alt: true))
            }
        }
        .padding(28)
    }

    private func open(_ door: Door, role: Role) {
        let session = Session(door: door, role: role)
        if let loc = location.last {
            session.startLat = loc.coordinate.latitude
            session.startLon = loc.coordinate.longitude
            session.startAccuracy = loc.horizontalAccuracy
            session.startGpsQuality = location.quality
        }
        context.insert(session)
        let name = role == .base ? "BASE · YOU" : role == .scout ? "SCOUT · YOU" : "HUB · YOU"
        context.insert(FieldNode(sessionId: session.id, role: role, name: name, coordinate: session.startCoordinate))
        if door == .broadcast {
            let room = BroadcastRoom(sessionId: session.id, title: "Field broadcast")
            session.broadcastId = room.id
            context.insert(room)
        }
        sync.enqueue(context: context, type: "session.open", payload: [
            "sessionId": session.id.uuidString,
            "invite": session.inviteCode,
        ])
        try? context.save()
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
        return HStack {
            VStack(alignment: .leading) {
                Text(last == nil ? "LIVE FIELD" : "FIELD NOTE · NON-HUMAN").font(.system(size: 8)).foregroundStyle(.secondary)
                Text(last?.label ?? "Listening for the wild").font(.subheadline.bold())
                Text(last == nil ? "No invented animals. UNKNOWN stays UNKNOWN." : ListenerCopy.sharingIsNotContributing)
                    .font(.system(size: 10)).foregroundStyle(.secondary)
            }
            Spacer()
            Text(last?.contributed == true ? "IN LIBRARY" : "PRIVATE\nON DEVICE")
                .font(.system(size: 8)).foregroundStyle(Color(red: 0.49, green: 1, blue: 0.65))
        }
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 17))
        .padding(.horizontal)
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
        let enc = Encounter(sessionId: session.id, label: kind == .mystery ? "UNKNOWN" : (text.isEmpty ? kind.rawValue.uppercased() : text))
        enc.lat = note.lat
        enc.lon = note.lon
        enc.originalAudioPath = mediaPath
        if human { enc.excludeAsHuman() }
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
