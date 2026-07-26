-- Publish compositor variables before portals and desktop services are started.
hl.on("hyprland.start", function()
    -- exec_cmd does not perform shell tilde expansion; use the installed
    -- absolute entrypoint so UWSM sessions always publish their environment.
    hl.exec_cmd("/home/colutti/.local/bin/colutti-session-init")
end)

hl.on("hyprland.shutdown", function()
    hl.exec_cmd("systemctl --user stop dms")
end)
