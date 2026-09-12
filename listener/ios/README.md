# LISTENER — iPhone (Xcode)

Open this folder on a Mac:

```text
listener/ios/Listener.xcodeproj
```

- Display name: **LISTENER**
- Bundle ID: `tech.primefield.listener`
- Stack: SwiftUI, SwiftData, MapKit, Core Location, AVFoundation, PhotosUI / share sheet

This Linux environment cannot enroll in the Apple Developer Program or upload a build. The Swift project is the App Store starting point.

## Honest status

We cannot complete Apple enrollment ($99/year) or TestFlight upload from this VM.

## Mac / Xcode / TestFlight steps

1. Install **Xcode 15+** from the Mac App Store.
2. Sign in to Xcode with the Apple ID that will enroll at [developer.apple.com/programs](https://developer.apple.com/programs) ($99/year).
3. Open `Listener.xcodeproj`. Set **Signing & Capabilities** → Team to your paid team. Keep bundle id `tech.primefield.listener`.
4. Host `listener/app/privacy.html` at a public HTTPS URL. Put that URL in App Store Connect privacy and in the listing.
5. Plug in an iPhone, or pick an iPhone 15/16 simulator. Run (⌘R). Grant **Location While Using** and **Microphone** when asked.
6. Product → Archive. In the Organizer, **Distribute App** → App Store Connect → Upload.
7. In [App Store Connect](https://appstoreconnect.apple.com): create the LISTENER app (bundle `tech.primefield.listener`), paste listing copy from `listener/store/APP-STORE.md`, attach screenshots from an iPhone, add the privacy URL.
8. Add the uploaded build to **TestFlight**. Invite testers. After review, submit for App Store review.

RETURN is a safety aid, not a replacement for Maps or a compass you already trust.
