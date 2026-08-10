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

-- The calibration window writes this one-monitor override atomically.  The
-- fallback above stays SDR until the user explicitly saves a calibration.
local state = os.getenv("XDG_STATE_HOME") or (os.getenv("HOME") .. "/.local/state")
local calibration = state .. "/colutti-desktop/generated/hdr-calibration.lua"
local calibration_chunk = loadfile(calibration)
if calibration_chunk then
    calibration_chunk()
end

hl.config({
    render = {
        cm_auto_hdr = 2,
    },
    quirks = {
        -- Some HDR games (including Proton titles) only expose their HDR option
        -- when the compositor advertises HDR before the game starts.
        prefer_hdr = 1,
    },
})
