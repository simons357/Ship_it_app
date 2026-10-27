import SwiftData
import SwiftUI

@main
struct ListenerApp: App {
    var body: some Scene {
        WindowGroup {
            RootView()
        }
        .modelContainer(for: [
            Session.self,
            Breadcrumb.self,
            FieldNode.self,
            FieldNote.self,
            Encounter.self,
            ListenerCard.self,
            LibraryContribution.self,
            BroadcastRoom.self,
            SyncEvent.self,
            DevicePair.self,
        ])
    }
}
