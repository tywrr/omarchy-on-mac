// Local searchable PDF panel. Global hotkeys belong to skhd, not this app.
import AppKit
import PDFKit

enum Sheet: String {
    case mac, herdr

    var title: String { self == .mac ? "macOS keybindings" : "Herdr keybindings" }
    var filename: String {
        self == .mac ? "omarchy-on-mac-keybindings-dark" : "herdr-keybindings-omarchy-dark"
    }
}

final class KeysPanel: NSPanel {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { false }
}

final class AppDelegate: NSObject, NSApplicationDelegate, NSSearchFieldDelegate, NSWindowDelegate {
    private var panel: KeysPanel!
    private let pdf = PDFView()
    private let search = NSSearchField()
    private let titleLabel = NSTextField(labelWithString: "")
    private let countLabel = NSTextField(labelWithString: "")
    private var documents: [Sheet: PDFDocument] = [:]
    private var sheet: Sheet?
    private var matches: [PDFSelection] = []
    private var matchIndex = 0
    private var previousApp: NSRunningApplication?
    private var keyMonitor: Any?
    private var pendingSearch: DispatchWorkItem?

    override init() {
        super.init()
        NSWorkspace.shared.notificationCenter.addObserver(
            self, selector: #selector(otherAppActivated(_:)),
            name: NSWorkspace.didActivateApplicationNotification, object: nil
        )
    }

    @objc private func otherAppActivated(_ notification: Notification) {
        if let application = notification.userInfo?[NSWorkspace.applicationUserInfoKey] as? NSRunningApplication,
           application.processIdentifier != ProcessInfo.processInfo.processIdentifier {
            previousApp = application
        }
    }

    func applicationDidFinishLaunching(_ notification: Notification) {
        preparePanel()
        // URL events also reach a running instance; keep the panel ready while hidden.
    }

    func application(_ application: NSApplication, open urls: [URL]) {
        guard let url = urls.last, url.scheme == "omarchy-keys",
              let requested = Sheet(rawValue: url.host ?? "") else { return }
        preparePanel()
        if panel.isVisible, sheet == requested, NSApp.isActive {
            dismiss()
        } else {
            show(requested)
        }
    }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows: Bool) -> Bool {
        // `open -a ... URL` may also send a reopen event. Only the URL chooses
        // the sheet, so a single hotkey cannot accidentally show then hide it.
        return false
    }

    private func preparePanel() {
        guard panel == nil else { return }
        let background = NSColor(srgbRed: 24 / 255, green: 25 / 255, blue: 35 / 255, alpha: 1)
        panel = KeysPanel(
            contentRect: NSRect(x: 0, y: 0, width: 1060, height: 872),
            styleMask: [.titled, .closable, .resizable, .fullSizeContentView],
            backing: .buffered, defer: false
        )
        panel.titleVisibility = .hidden
        panel.titlebarAppearsTransparent = true
        panel.isReleasedWhenClosed = false
        panel.hidesOnDeactivate = false
        panel.level = .floating
        panel.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .ignoresCycle]
        panel.appearance = NSAppearance(named: .darkAqua)
        panel.backgroundColor = background
        panel.contentMinSize = NSSize(width: 640, height: 520)
        panel.standardWindowButton(.miniaturizeButton)?.isHidden = true
        panel.standardWindowButton(.zoomButton)?.isHidden = true
        panel.delegate = self
        panel.setAccessibilityIdentifier("omarchy-keys-panel")

        guard let content = panel.contentView else { return }
        titleLabel.font = .systemFont(ofSize: 13, weight: .semibold)
        titleLabel.setContentHuggingPriority(.defaultHigh, for: .horizontal)
        search.placeholderString = "Search shortcuts"
        search.sendsSearchStringImmediately = true
        search.sendsWholeSearchString = false
        search.delegate = self
        search.setAccessibilityIdentifier("shortcut-search")
        countLabel.font = .monospacedDigitSystemFont(ofSize: 11, weight: .regular)
        countLabel.textColor = .secondaryLabelColor
        countLabel.alignment = .right
        countLabel.setContentHuggingPriority(.required, for: .horizontal)
        let hint = NSTextField(labelWithString: "↵ next  ·  Esc close")
        hint.font = .systemFont(ofSize: 11)
        hint.textColor = .secondaryLabelColor
        hint.setContentHuggingPriority(.required, for: .horizontal)
        let bar = NSStackView(views: [titleLabel, search, countLabel, hint])
        bar.orientation = .horizontal
        bar.alignment = .centerY
        bar.spacing = 16
        bar.translatesAutoresizingMaskIntoConstraints = false
        content.addSubview(bar)

        pdf.translatesAutoresizingMaskIntoConstraints = false
        pdf.autoScales = true
        pdf.displayMode = .singlePage
        pdf.displaysPageBreaks = false
        pdf.pageShadowsEnabled = false
        pdf.backgroundColor = background
        content.addSubview(pdf)
        NSLayoutConstraint.activate([
            bar.leadingAnchor.constraint(equalTo: content.leadingAnchor, constant: 72),
            bar.trailingAnchor.constraint(equalTo: content.trailingAnchor, constant: -16),
            bar.topAnchor.constraint(equalTo: content.topAnchor),
            bar.heightAnchor.constraint(equalToConstant: 52),
            search.widthAnchor.constraint(greaterThanOrEqualToConstant: 160),
            pdf.topAnchor.constraint(equalTo: bar.bottomAnchor),
            pdf.leadingAnchor.constraint(equalTo: content.leadingAnchor),
            pdf.trailingAnchor.constraint(equalTo: content.trailingAnchor),
            pdf.bottomAnchor.constraint(equalTo: content.bottomAnchor),
        ])

        keyMonitor = NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            guard let self, self.panel.isVisible else { return event }
            let command = event.modifierFlags.contains(.command)
            if event.keyCode == 53 || (command && event.keyCode == 13) {
                self.dismiss()
                return nil
            }
            if command && event.keyCode == 3 {
                self.focusSearch()
                return nil
            }
            if (command && event.keyCode == 5)
                || ([36, 76].contains(event.keyCode) && self.search.currentEditor() != nil) {
                self.nextMatch(backwards: event.modifierFlags.contains(.shift))
                return nil
            }
            return event
        }
        let menu = NSMenu()
        let appItem = NSMenuItem()
        menu.addItem(appItem)
        appItem.submenu = NSMenu()
        appItem.submenu?.addItem(withTitle: "Quit Omarchy Keys", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        let editItem = NSMenuItem()
        menu.addItem(editItem)
        editItem.submenu = NSMenu(title: "Edit")
        for (title, selector, key) in [
            ("Cut", "cut:", "x"), ("Copy", "copy:", "c"),
            ("Paste", "paste:", "v"), ("Select All", "selectAll:", "a"),
        ] {
            editItem.submenu?.addItem(withTitle: title, action: Selector(selector), keyEquivalent: key)
        }
        NSApp.mainMenu = menu
    }

    private func show(_ requested: Sheet) {
        preparePanel()
        if let frontmost = NSWorkspace.shared.frontmostApplication,
           frontmost.processIdentifier != ProcessInfo.processInfo.processIdentifier {
            previousApp = frontmost
        }
        if documents[requested] == nil {
            guard let url = Bundle.main.url(forResource: requested.filename, withExtension: "pdf"),
                  let document = PDFDocument(url: url) else {
                let alert = NSAlert()
                alert.messageText = "The shortcut sheet could not be opened."
                alert.informativeText = "Reinstall Omarchy Keys from the repository."
                alert.runModal()
                return
            }
            documents[requested] = document
        }
        sheet = requested
        panel.title = requested.title
        titleLabel.stringValue = requested.title
        pdf.document = documents[requested]
        search.stringValue = ""
        updateSearch()
        let screen = NSScreen.screens.first { NSMouseInRect(NSEvent.mouseLocation, $0.frame, false) }
            ?? NSScreen.main
        if let area = screen?.visibleFrame {
            let width = min(1100, area.width - 64, (area.height - 128) * 792 / 612)
            let height = width * 612 / 792 + 52
            panel.setFrame(NSRect(x: area.midX - width / 2, y: area.midY - height / 2,
                                  width: width, height: height), display: false)
        }
        // Finish handling the URL before requesting focus. In particular, the
        // first URL can arrive before applicationDidFinishLaunching.
        DispatchQueue.main.async { [self] in
            NSApp.unhide(nil)
            NSApp.activate(ignoringOtherApps: true)
            panel.makeKeyAndOrderFront(nil)
            pdf.autoScales = true
            focusSearch()
        }
    }

    private func focusSearch() {
        panel.makeFirstResponder(search)
        search.selectText(nil)
    }

    func controlTextDidChange(_ notification: Notification) {
        pendingSearch?.cancel()
        let work = DispatchWorkItem { [weak self] in self?.updateSearch() }
        pendingSearch = work
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.08, execute: work)
    }

    private func updateSearch() {
        let query = search.stringValue.trimmingCharacters(in: .whitespacesAndNewlines)
        matches = query.isEmpty ? [] : pdf.document?.findString(query, withOptions: [.caseInsensitive, .diacriticInsensitive]) ?? []
        matchIndex = 0
        highlightMatches()
        if query.isEmpty { countLabel.stringValue = "" }
        else if matches.isEmpty { countLabel.stringValue = "No matches" }
    }

    private func highlightMatches() {
        for (index, match) in matches.enumerated() {
            match.color = (index == matchIndex ? NSColor.systemOrange : .systemYellow).withAlphaComponent(0.55)
        }
        pdf.highlightedSelections = matches
        guard !matches.isEmpty else { return }
        pdf.go(to: matches[matchIndex])
        countLabel.stringValue = "\(matchIndex + 1) / \(matches.count)"
    }

    private func nextMatch(backwards: Bool) {
        guard !matches.isEmpty else { return }
        matchIndex = (matchIndex + (backwards ? matches.count - 1 : 1)) % matches.count
        highlightMatches()
    }

    private func dismiss() {
        pendingSearch?.cancel()
        let restoreFocus = NSApp.isActive
        panel.orderOut(nil)
        NSApp.hide(nil)
        if restoreFocus, let previousApp, !previousApp.isTerminated {
            previousApp.activate(options: [])
        }
    }

    func windowShouldClose(_ sender: NSWindow) -> Bool {
        dismiss()
        return false
    }

    func applicationDidResignActive(_ notification: Notification) {
        pendingSearch?.cancel()
        panel?.orderOut(nil)
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.setActivationPolicy(.accessory)
app.delegate = delegate
app.run()
