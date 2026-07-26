-- UWSM owns XDG and toolkit environment. Keep compositor config session-local.
hl.env("XCURSOR_THEME", "Breeze")
hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_THEME", "BreezeX")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("MOZ_ENABLE_WAYLAND", "1")
hl.env("ELECTRON_OZONE_PLATFORM_HINT", "auto")
-- Use KDE's native Qt platform theme so Qt applications share the KDE palette.
-- This stays Hyprland-local so the Plasma fallback keeps its native integration.
hl.env("QT_QPA_PLATFORMTHEME", "kde")
hl.env("QT_QPA_PLATFORMTHEME_QT6", "kde")
-- Steam is an XWayland client; 2x keeps its CEF UI readable on the 4K DP-2 display.
hl.env("STEAM_FORCE_DESKTOPUI_SCALING", "2")
