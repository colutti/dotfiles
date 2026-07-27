hl.window_rule({
    name = "steam-ui-scale",
    match = { initial_class = "steam", xwayland = true },
    nearest_neighbor = false,
})

hl.window_rule({
    name = "steam-main-placement",
    match = { initial_class = "steam", initial_title = "Steam" },
    workspace = "4 silent",
    monitor = "DP-2",
})

hl.window_rule({
    name = "game-content",
    match = { content = "game" },
    immediate = true,
})

hl.window_rule({
    name = "gamescope-placement",
    match = { initial_class = "gamescope" },
    workspace = "4 silent",
    monitor = "DP-2",
})

hl.window_rule({
    name = "chat-telegram-placement",
    match = { initial_class = "org.telegram.desktop" },
    workspace = "6 silent",
    monitor = "HDMI-A-1",
})

hl.window_rule({
    name = "chat-discord-placement",
    match = { initial_class = "discord" },
    workspace = "6 silent",
    monitor = "HDMI-A-1",
})

hl.window_rule({
    name = "zen-compositor-border",
    match = { initial_class = "app.zen_browser.zen" },
    border_size = 1,
})

hl.window_rule({
    name = "settings-dialog",
    match = { initial_title = "Colutti Desktop" },
    float = true,
    size = "1040 720",
    center = true,
})

hl.layer_rule({
    name = "shell-blur",
    match = { namespace = "quickshell" },
    blur = true,
    blur_popups = true,
    ignore_alpha = 0.78,
})
