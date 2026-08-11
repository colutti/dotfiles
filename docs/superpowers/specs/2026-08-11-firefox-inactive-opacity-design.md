# Zen Browser inactive opacity

## Goal

Keep Zen Browser fully opaque when it loses focus without changing the inactive-opacity
behavior of any other application.

## Design

Add one declarative Hyprland window rule in `hyprland/.config/hypr/modules/rules.lua`.
It matches Zen Browser's initial class (`app.zen_browser.zen`) and sets both active and inactive
opacity to `1.0`.

The global `decoration.inactive_opacity = 0.96` remains unchanged, so all other
windows retain the current visual behavior. The rule does not modify blur, focus,
window placement, or other Zen Browser properties.

## Verification

Run Hyprland's configuration verifier against the sole entrypoint. Then reload the
live configuration and inspect the rule list or observe a focused-to-unfocused Zen Browser
transition if an active Hyprland session is available.
