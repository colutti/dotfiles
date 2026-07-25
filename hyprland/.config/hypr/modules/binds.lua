local app = function(command)
    return hl.dsp.exec_cmd("uwsm app -- " .. command)
end

hl.bind("SUPER + Return", app("alacritty"), { description = "Terminal" })
hl.bind(
    "SUPER + E",
    app("env QT_QPA_PLATFORMTHEME=kde dolphin"),
    { description = "Files" }
)
hl.bind("SUPER + Space", app("fuzzel"), { description = "Launcher" })
hl.bind("SUPER + N", app("swaync-client -t -sw"), { description = "Notifications and controls" })
hl.bind("SUPER + comma", app("colutti-theme-menu"), { description = "Theme selector" })
hl.bind("SUPER + I", app("colutti-settings-gui"), { description = "Desktop settings" })
hl.bind("SUPER + SHIFT + V", app("colutti-clipboard-menu"), { description = "Clipboard history" })
hl.bind("ALT + Q", hl.dsp.window.close(), { description = "Close window" })
hl.bind("SUPER + C", hl.dsp.window.close(), { description = "Close window" })
hl.bind("SUPER + F", hl.dsp.window.fullscreen(), { description = "Fullscreen" })
hl.bind("SUPER + V", hl.dsp.window.float({ action = "toggle" }), { description = "Toggle float" })
hl.bind("SUPER + L", hl.dsp.exec_cmd("loginctl lock-session"), { description = "Lock" })
hl.bind("Print", hl.dsp.exec_cmd("grim -g \"$(slurp)\" - | satty --filename -"), { description = "Region screenshot" })

hl.bind("SUPER + Left", hl.dsp.focus({ direction = "l" }), { description = "Focus left" })
hl.bind("SUPER + Right", hl.dsp.focus({ direction = "r" }), { description = "Focus right" })
hl.bind("SUPER + Up", hl.dsp.focus({ direction = "u" }), { description = "Focus up" })
hl.bind("SUPER + Down", hl.dsp.focus({ direction = "d" }), { description = "Focus down" })
hl.bind("SUPER + SHIFT + Left", hl.dsp.window.move({ direction = "l" }), { description = "Move window left" })
hl.bind("SUPER + SHIFT + Right", hl.dsp.window.move({ direction = "r" }), { description = "Move window right" })
hl.bind("SUPER + SHIFT + Up", hl.dsp.window.move({ direction = "u" }), { description = "Move window up" })
hl.bind("SUPER + SHIFT + Down", hl.dsp.window.move({ direction = "d" }), { description = "Move window down" })

for i = 1, 8 do
    hl.bind("SUPER + " .. i, hl.dsp.focus({ workspace = i }))
    hl.bind("SUPER + SHIFT + " .. i, hl.dsp.window.move({ workspace = i }))
end

hl.bind("SUPER + mouse_down", hl.dsp.focus({ workspace = "m+1" }))
hl.bind("SUPER + mouse_up", hl.dsp.focus({ workspace = "m-1" }))
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
hl.bind("mouse:275", hl.dsp.focus({ workspace = "m-1" }))
hl.bind("mouse:276", hl.dsp.focus({ workspace = "m+1" }))

hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("colutti-audio-control raise"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("colutti-audio-control lower"), { locked = true, repeating = true })
hl.bind("XF86AudioMute", hl.dsp.exec_cmd("colutti-audio-control mute"), { locked = true })
hl.bind("XF86AudioMicMute", hl.dsp.exec_cmd("colutti-audio-control mic-mute"), { locked = true })
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("colutti-audio-control play"), { locked = true })
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("colutti-audio-control next"), { locked = true })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("colutti-audio-control previous"), { locked = true })
