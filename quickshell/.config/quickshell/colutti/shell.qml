import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Quickshell
import Quickshell.Hyprland
import Quickshell.Io
import Quickshell.Services.SystemTray

ShellRoot {
    id: root

    property string clockText: ""
    property string metricsText: "CPU · RAM · GPU"
    property string statusText: "NET · TS · VOL · MIC · PWR"
    property color background: "#111817"
    property color surface: "#172220"
    property color surfaceAlt: "#20302d"
    property color text: "#e7f0ec"
    property color muted: "#9aaba5"
    property color accent: "#41c7b0"
    property color warning: "#e5a84b"
    property color critical: "#ef776f"
    property color outline: "#38514c"
    property string panelLayout: "islands"
    property string panelMaterial: "solid"
    property int animationMs: 180
    property int panelRadius: 14
    property int panelMargin: 4
    property real panelOpacity: 0.96
    property bool gameMode: false

    function loadTheme() {
        try {
            const parsed = JSON.parse(themeFile.text())
            const palette = parsed.palette
            const panel = parsed.panel
            root.background = palette.background
            root.surface = palette.surface
            root.surfaceAlt = palette.surface_alt
            root.text = palette.text
            root.muted = palette.muted
            root.accent = palette.accent
            root.warning = palette.warning
            root.critical = palette.critical
            root.outline = palette.outline
            root.panelLayout = panel.layout
            root.panelMaterial = panel.material
            root.animationMs = panel.animation_ms
            const personalities = {
                islands: { radius: 14, margin: 4, opacity: 0.96 },
                rail: { radius: 4, margin: 0, opacity: 0.82 },
                studio: { radius: 8, margin: 3, opacity: 0.98 },
                architect: { radius: 3, margin: 6, opacity: 1.0 },
                canopy: { radius: 18, margin: 5, opacity: 0.94 }
            }
            const personality = personalities[panel.layout] || personalities.islands
            root.panelRadius = personality.radius
            root.panelMargin = personality.margin
            root.panelOpacity = personality.opacity
        } catch (error) {
            console.warn("Keeping built-in Aurora Forge tokens:", error)
        }
    }

    function run(command) {
        Quickshell.execDetached(["sh", "-lc", command])
    }

    Process {
        id: clockProcess
        command: ["date", "+%a %d %b  %H:%M"]
        running: true
        stdout: StdioCollector {
            onStreamFinished: root.clockText = text.trim()
        }
    }

    FileView {
        id: themeFile
        path: (Quickshell.env("XDG_STATE_HOME") || Quickshell.env("HOME") + "/.local/state")
              + "/colutti-desktop/generated/theme.json"
        watchChanges: true
        printErrors: false
        onLoaded: root.loadTheme()
        onFileChanged: reload()
    }

    FileView {
        id: settingsFile
        path: (Quickshell.env("XDG_CONFIG_HOME") || Quickshell.env("HOME") + "/.config")
              + "/colutti-desktop/settings.json"
        watchChanges: true
        printErrors: false
        onLoaded: {
            try {
                root.gameMode = JSON.parse(text()).profile.game === "on"
            } catch (error) {
                root.gameMode = false
            }
        }
        onFileChanged: reload()
    }

    Process {
        id: metricsProcess
        command: [Quickshell.env("HOME") + "/.local/bin/colutti-metrics-line"]
        running: true
        stdout: StdioCollector {
            onStreamFinished: {
                const value = text.trim()
                if (value !== "") root.metricsText = value
            }
        }
    }

    Process {
        id: statusProcess
        command: [Quickshell.env("HOME") + "/.local/bin/colutti-status-line"]
        running: true
        stdout: StdioCollector {
            onStreamFinished: {
                const value = text.trim()
                if (value !== "") root.statusText = value
            }
        }
    }

    Timer {
        interval: 1000
        repeat: true
        running: true
        onTriggered: clockProcess.running = true
    }

    Timer {
        interval: 5000
        repeat: true
        running: true
        onTriggered: {
            metricsProcess.running = true
            statusProcess.running = true
        }
    }

    Variants {
        model: Quickshell.screens.filter(screen => screen.name === "DP-2")

        PanelWindow {
            id: bar
            required property var modelData
            screen: modelData
            color: "transparent"
            implicitHeight: 44
            anchors { top: true; left: true; right: true }

            Rectangle {
                anchors { fill: parent; margins: root.panelMargin }
                radius: root.panelRadius
                color: Qt.rgba(root.surface.r, root.surface.g, root.surface.b, root.panelOpacity)
                border.width: 1
                border.color: root.outline

                RowLayout {
                    anchors { fill: parent; leftMargin: 10; rightMargin: 10 }
                    spacing: 8

                    Rectangle {
                        implicitWidth: 34
                        implicitHeight: 30
                        radius: 9
                        color: root.surfaceAlt
                        Text {
                            anchors.centerIn: parent
                            text: "⌘"
                            color: root.text
                            font.pixelSize: 17
                            font.bold: true
                        }
                        MouseArea { anchors.fill: parent; onClicked: root.run("fuzzel") }
                    }

                    RowLayout {
                        spacing: 4
                        Repeater {
                            model: Hyprland.workspaces.values.filter(workspace =>
                                workspace.id > 0 && workspace.id <= 8 &&
                                (!workspace.monitor || workspace.monitor.name === bar.screen.name))
                            Rectangle {
                                required property var modelData
                                implicitWidth: modelData.active ? 38 : 28
                                implicitHeight: 28
                                radius: 9
                                color: modelData.active ? root.accent : root.surfaceAlt
                                Text {
                                    anchors.centerIn: parent
                                    text: modelData.id
                                    color: modelData.active ? root.background : root.text
                                    font.pixelSize: 13
                                    font.bold: modelData.active
                                }
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: modelData.activate()
                                }
                            }
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        horizontalAlignment: Text.AlignHCenter
                        elide: Text.ElideRight
                        text: root.metricsText + "  ·  " + root.statusText
                        color: root.text
                        font.family: "JetBrainsMono Nerd Font"
                        font.pixelSize: 10
                    }

                    RowLayout {
                        spacing: 5
                        Repeater {
                            model: SystemTray.items.values
                            Image {
                                required property var modelData
                                source: modelData.icon
                                sourceSize.width: 18
                                sourceSize.height: 18
                                Layout.preferredWidth: 24
                                Layout.preferredHeight: 24
                                MouseArea {
                                    id: trayMouse
                                    anchors.fill: parent
                                    acceptedButtons: Qt.LeftButton | Qt.RightButton
                                    onClicked: mouse => {
                                        if (mouse.button === Qt.RightButton || modelData.onlyMenu) {
                                            const point = trayMouse.mapToItem(
                                                bar.contentItem, mouse.x, mouse.y
                                            )
                                            modelData.display(bar, point.x, point.y)
                                        } else {
                                            modelData.activate()
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        implicitWidth: clockLabel.implicitWidth + 18
                        implicitHeight: 30
                        radius: 9
                        color: root.surfaceAlt
                        Text {
                            id: clockLabel
                            anchors.centerIn: parent
                            text: root.clockText
                            color: root.text
                            font.pixelSize: 13
                            font.weight: Font.DemiBold
                        }
                        MouseArea {
                            anchors.fill: parent
                            acceptedButtons: Qt.LeftButton
                            preventStealing: true
                            onPressed: {
                                root.run("swaync-client -t -sw")
                            }
                        }
                    }
                }
            }
        }
    }

    Variants {
        model: Quickshell.screens.filter(screen => screen.name === "HDMI-A-1")

        PanelWindow {
            required property var modelData
            screen: modelData
            visible: root.gameMode
            color: "transparent"
            implicitWidth: 760
            implicitHeight: 20
            anchors { bottom: true }
            margins { bottom: 1 }
            exclusiveZone: 0

            Rectangle {
                anchors.fill: parent
                radius: 7
                color: Qt.rgba(root.background.r, root.background.g, root.background.b, 0.90)
                border.width: 1
                border.color: root.outline
                Text {
                    anchors.centerIn: parent
                    text: "GAME · " + root.metricsText
                    color: root.text
                    font.family: "JetBrainsMono Nerd Font"
                    font.pixelSize: 10
                    font.weight: Font.DemiBold
                }
            }
        }
    }

}
