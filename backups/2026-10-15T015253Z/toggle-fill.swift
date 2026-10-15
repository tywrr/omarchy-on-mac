// Native window/menu actions and Accessibility Zoom reset.
// Requires English app menu titles and Accessibility access for the caller.
import AppKit
import ApplicationServices

struct Failure: Error, CustomStringConvertible {
    let description: String
}

func attribute(_ element: AXUIElement, _ name: String) throws -> CFTypeRef {
    var value: CFTypeRef?
    let result = AXUIElementCopyAttributeValue(element, name as CFString, &value)
    guard result == .success, let value else {
        throw Failure(description: "Cannot read \(name): \(result.rawValue)")
    }
    return value
}

func child(_ element: AXUIElement, titled title: String? = nil) throws -> AXUIElement {
    let children = try attribute(element, kAXChildrenAttribute) as! [AXUIElement]
    guard let found = children.first(where: {
        title == nil || (try? attribute($0, kAXTitleAttribute) as? String) == title
    }) else {
        throw Failure(description: "Native menu item unavailable: \(title ?? "submenu")")
    }
    return found
}

func enabled(_ element: AXUIElement) -> Bool {
    (try? attribute(element, kAXEnabledAttribute) as? Bool) == true
}

func press(_ element: AXUIElement) throws {
    let result = AXUIElementPerformAction(element, kAXPressAction as CFString)
    guard result == .success else {
        throw Failure(description: "Cannot invoke native menu action: \(result.rawValue)")
    }
}

func frame(_ window: AXUIElement) throws -> CGRect {
    let position = try attribute(window, kAXPositionAttribute) as! AXValue
    let size = try attribute(window, kAXSizeAttribute) as! AXValue
    var point = CGPoint.zero
    var dimensions = CGSize.zero
    guard AXValueGetValue(position, .cgPoint, &point),
          AXValueGetValue(size, .cgSize, &dimensions) else {
        throw Failure(description: "Cannot read focused window geometry")
    }
    return CGRect(origin: point, size: dimensions)
}

func toggleFill() throws {
    guard let app = NSWorkspace.shared.frontmostApplication else { return }
    let process = AXUIElementCreateApplication(app.processIdentifier)
    let window = try attribute(process, kAXFocusedWindowAttribute) as! AXUIElement
    guard (try? attribute(window, kAXSubroleAttribute) as? String) == kAXStandardWindowSubrole,
          (try? attribute(window, "AXFullScreen") as? Bool) != true else { return }

    let menuBar = try attribute(process, kAXMenuBarAttribute) as! AXUIElement
    let windowItem = try child(menuBar, titled: "Window")
    let menu = try child(windowItem)
    let fill = try child(menu, titled: "Fill")
    guard enabled(fill) else { return }

    let before = try frame(window)
    try press(fill)
    Thread.sleep(forTimeInterval: 0.25)
    // Repeated Fill preserves the native restore history. If it did not move
    // or resize this window, use that history to restore its previous size.
    if try frame(window) == before {
        let move = try child(menu, titled: "Move & Resize")
        let restore = try child(child(move), titled: "Return to Previous Size")
        if enabled(restore) { try press(restore) }
    }
}

func toggleFullScreen() throws {
    guard let app = NSWorkspace.shared.frontmostApplication else { return }
    let process = AXUIElementCreateApplication(app.processIdentifier)
    let window = try attribute(process, kAXFocusedWindowAttribute) as! AXUIElement
    let isFullScreen = try attribute(window, "AXFullScreen") as! Bool
    let result = AXUIElementSetAttributeValue(
        window, "AXFullScreen" as CFString,
        isFullScreen ? kCFBooleanFalse : kCFBooleanTrue
    )
    guard result == .success else {
        throw Failure(description: "Cannot toggle native full screen: \(result.rawValue)")
    }
}

func newFinderWindow() throws {
    guard let finder = NSRunningApplication.runningApplications(withBundleIdentifier: "com.apple.finder").first else {
        throw Failure(description: "Finder is not running")
    }
    let process = AXUIElementCreateApplication(finder.processIdentifier)
    let menuBar = try attribute(process, kAXMenuBarAttribute) as! AXUIElement
    let fileItem = try child(menuBar, titled: "File")
    let newWindow = try child(child(fileItem), titled: "New Finder Window")
    try press(newWindow)
    finder.activate(options: [])
}

func showAppleMenu() throws {
    guard let app = NSWorkspace.shared.frontmostApplication else { return }
    let process = AXUIElementCreateApplication(app.processIdentifier)
    let menuBar = try attribute(process, kAXMenuBarAttribute) as! AXUIElement
    // macOS puts the Apple menu first, independently of the app or language.
    try press(child(menuBar))
}

func resetZoom() throws {
    // The public Universal Access API is false when fully zoomed out. Avoid
    // toggling native Zoom back in when the user is already at normal scale.
    guard UAZoomEnabled() else { return }
    // Post native Option+Command+8 through the already-authorized skhd binary.
    // This avoids requiring event-posting permission for a separate helper.
    let command = Process()
    command.executableURL = URL(fileURLWithPath: "/usr/bin/env")
    command.arguments = ["skhd", "--key", "alt + cmd - 8"]
    try command.run()
    command.waitUntilExit()
    guard command.terminationStatus == 0 else {
        throw Failure(description: "skhd could not post the native Zoom toggle")
    }
}

do {
    switch CommandLine.arguments.dropFirst().first {
    case "--apple-menu":
        try showAppleMenu()
    case "--new-finder-window":
        try newFinderWindow()
    case "--fullscreen":
        try toggleFullScreen()
    case "--zoom-reset":
        try resetZoom()
    case nil:
        try toggleFill()
    default:
        throw Failure(description: "Unknown native helper action")
    }
} catch {
    FileHandle.standardError.write(Data("toggle-fill: \(error)\n".utf8))
    exit(1)
}
