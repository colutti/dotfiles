-- Publish compositor variables before portals and desktop services are started.
hl.on("hyprland.start", function()
    hl.exec_cmd("~/.local/bin/colutti-session-init")
end)

hl.on("hyprland.shutdown", function()
    hl.exec_cmd("systemctl --user stop colutti-desktop.target")
end)
