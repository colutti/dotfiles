local workspaces = {
    { id = 1, name = "Web", monitor = "DP-2", default = true },
    { id = 2, name = "Code", monitor = "DP-2" },
    { id = 3, name = "Media", monitor = "DP-2" },
    { id = 4, name = "Games", monitor = "DP-2" },
    { id = 5, name = "Focus", monitor = "DP-2" },
    { id = 6, name = "Chat", monitor = "HDMI-A-1", default = true },
    { id = 7, name = "Music", monitor = "HDMI-A-1" },
    { id = 8, name = "Monitor", monitor = "HDMI-A-1" },
}

for _, workspace in ipairs(workspaces) do
    hl.workspace_rule({
        workspace = workspace.id,
        monitor = workspace.monitor,
        default = workspace.default or false,
        persistent = true,
    })
end
