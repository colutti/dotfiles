hl.config({
    general = {
        gaps_in = 10,
        gaps_out = 20,
        border_size = 1,
        col = {
            active_border = "rgba(41c7b0ff)",
            inactive_border = "rgba(38514cff)",
        },
        resize_on_border = true,
        allow_tearing = false,
        layout = "dwindle",
    },
    decoration = {
        rounding = 12,
        rounding_power = 2,
        active_opacity = 1.0,
        inactive_opacity = 0.96,
        blur = { enabled = true, size = 6, passes = 2, vibrancy = 0.12 },
        shadow = { enabled = true, range = 14, render_power = 3, color = "rgba(050a09aa)" },
    },
    animations = { enabled = false },
    dwindle = {
        preserve_split = true,
        force_split = 2,
    },
    misc = {
        disable_hyprland_logo = true,
        force_default_wallpaper = 0,
        focus_on_activate = true,
    },
    xwayland = { force_zero_scaling = true },
})

hl.curve("coluttiOut", { type = "bezier", points = {{0.16, 1}, {0.3, 1}} })
hl.animation({ leaf = "windows", enabled = false, speed = 4.4, bezier = "coluttiOut" })
hl.animation({ leaf = "layers", enabled = false, speed = 4.0, bezier = "coluttiOut" })
hl.animation({ leaf = "workspaces", enabled = false, speed = 3.6, bezier = "coluttiOut", style = "fade" })
