local app = function(command)
    return hl.dsp.exec_cmd("uwsm app -- " .. command)
end

local dms = function(...)
    return hl.dsp.exec_cmd("dms ipc call " .. table.concat({ ... }, " "))
end

hl.bind("SUPER + Return", app("kitty"), { description = "Terminal" })
hl.bind("SUPER + E", app("dolphin"), { description = "Files" })
hl.bind("SUPER + Space", dms("spotlight", "toggle"), { description = "Application launcher" })
hl.bind("SUPER + V", dms("clipboard", "toggle"), { description = "Clipboard history" })
hl.bind("SUPER + N", dms("notifications", "toggle"), { description = "Notification center" })
hl.bind("SUPER + comma", dms("settings", "focusOrToggle"), { description = "Settings" })
hl.bind("SUPER + M", dms("processlist", "focusOrToggle"), { description = "Process monitor" })
hl.bind("SUPER + Y", dms("dankdash", "wallpaper"), { description = "Wallpaper browser" })
hl.bind("SUPER + L", dms("lock", "lock"), { description = "Lock" })
hl.bind("SUPER + SHIFT + V", dms("clipboard", "toggle"), { description = "Clipboard history" })
hl.bind("SUPER + I", dms("settings", "focusOrToggle"), { description = "Hardware settings" })
hl.bind("SUPER + SHIFT + H", app("hdr-calibration"), {
    description = "HDR calibration",
})
hl.bind("ALT + Q", hl.dsp.window.close(), { description = "Close window" })
hl.bind("SUPER + C", hl.dsp.window.close(), { description = "Close window" })
hl.bind("SUPER + F", hl.dsp.window.fullscreen(), { description = "Fullscreen" })
hl.bind("SUPER + SHIFT + F", hl.dsp.window.float({ action = "toggle" }), {
    description = "Toggle floating window",
})
hl.bind("SUPER + Q", dms("settings", "focusOrToggle"), { description = "Settings" })
hl.bind("SUPER + O", dms("keybinds", "toggle", "hyprland"), { description = "Show keybinds" })
hl.bind("SUPER + P", dms("powermenu", "toggle"), { description = "Power menu" })
hl.bind("Print", hl.dsp.exec_cmd("grim -g \"$(slurp)\" - | wl-copy"), { description = "Screenshot region to clipboard" })

hl.bind("SUPER + Left", hl.dsp.focus({ direction = "l" }), { description = "Focus left" })
hl.bind("SUPER + Right", hl.dsp.focus({ direction = "r" }), { description = "Focus right" })
hl.bind("SUPER + Up", hl.dsp.focus({ direction = "u" }), { description = "Focus up" })
hl.bind("SUPER + Down", hl.dsp.focus({ direction = "d" }), { description = "Focus down" })
hl.bind("CTRL + SUPER + Up", hl.dsp.focus({ monitor = "DP-2" }), {
    description = "Focus main monitor",
})
hl.bind("CTRL + SUPER + Down", hl.dsp.focus({ monitor = "HDMI-A-1" }), {
    description = "Focus secondary monitor",
})
hl.bind("CTRL + SUPER + Left", hl.dsp.focus({ workspace = "m-1" }), {
    description = "Focus previous desktop on current monitor",
})
hl.bind("CTRL + SUPER + Right", hl.dsp.focus({ workspace = "m+1" }), {
    description = "Focus next desktop on current monitor",
})
hl.bind("SUPER + SHIFT + Left", hl.dsp.window.move({ direction = "l" }), { description = "Move window left" })
hl.bind("SUPER + SHIFT + Right", hl.dsp.window.move({ direction = "r" }), { description = "Move window right" })
hl.bind("SUPER + SHIFT + Up", hl.dsp.window.move({ direction = "u" }), { description = "Move window up" })
hl.bind("SUPER + SHIFT + Down", hl.dsp.window.move({ direction = "d" }), { description = "Move window down" })

hl.bind("SUPER + ALT + Left", hl.dsp.window.resize({ x = -20, y = 0, relative = true }), {
    description = "Resize window left",
    repeating = true,
})
hl.bind("SUPER + ALT + Right", hl.dsp.window.resize({ x = 20, y = 0, relative = true }), {
    description = "Resize window right",
    repeating = true,
})
hl.bind("SUPER + ALT + Up", hl.dsp.window.resize({ x = 0, y = -20, relative = true }), {
    description = "Resize window up",
    repeating = true,
})
hl.bind("SUPER + ALT + Down", hl.dsp.window.resize({ x = 0, y = 20, relative = true }), {
    description = "Resize window down",
    repeating = true,
})

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

hl.bind("XF86AudioRaiseVolume", dms("audio", "increment", "5"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", dms("audio", "decrement", "5"), { locked = true, repeating = true })
hl.bind("XF86AudioMute", dms("audio", "mute"), { locked = true })
hl.bind("XF86AudioMicMute", dms("mic", "mute"), { locked = true })
hl.bind("XF86MonBrightnessUp", dms("brightness", "increment", "5", ""), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", dms("brightness", "decrement", "5", ""), { locked = true, repeating = true })
