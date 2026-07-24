hl.monitor({
    output = "DP-2",
    mode = "3840x2160@60",
    position = "0x0",
    scale = 1.666667,
    bitdepth = 8,
    cm = "srgb",
    vrr = 0,
})

hl.monitor({
    output = "HDMI-A-1",
    mode = "1920x1080@60",
    position = "384x1296",
    scale = 1.25,
    bitdepth = 8,
    cm = "srgb",
    vrr = 0,
})

hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1 })

hl.config({
    render = {
        cm_auto_hdr = 1,
    },
})
