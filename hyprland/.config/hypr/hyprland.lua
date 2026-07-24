-- Colutti workstation entrypoint for Hyprland 0.56+.
-- Generated runtime values live outside this declarative module tree.
require("modules.monitors")
require("modules.environment")
require("modules.input")
require("modules.workspaces")
require("modules.rules")
require("modules.binds")
require("modules.appearance")
require("modules.permissions")
require("modules.autostart")

local stateHome = os.getenv("XDG_STATE_HOME") or (os.getenv("HOME") .. "/.local/state")
local generatedTheme = stateHome .. "/colutti-desktop/generated/hyprland-theme.lua"
local themeFile = io.open(generatedTheme, "r")
if themeFile then
    themeFile:close()
    dofile(generatedTheme)
end
