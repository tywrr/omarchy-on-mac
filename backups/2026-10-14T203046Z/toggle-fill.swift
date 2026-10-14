// Native Fill toggle and Apple menu action.
// Requires an English Window menu and Accessibility access for the caller.
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

func showAppleMenu() throws {
    guard let app = NSWorkspace.shared.frontmostApplication else { return }
    let process = AXUIElementCreateApplication(app.processIdentifier)
    let menuBar = try attribute(process, kAXMenuBarAttribute) as! AXUIElement
    // macOS puts the Apple menu first, independently of the app or language.
    try press(child(menuBar))
}

do {
    if CommandLine.arguments.dropFirst().first == "--apple-menu" {
        try showAppleMenu()
    } else {
        try toggleFill()
    }
} catch {
    FileHandle.standardError.write(Data("toggle-fill: \(error)\n".utf8))
    exit(1)
}
