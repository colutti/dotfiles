# Archived Theme Spec

Este documento registra uma especificação antiga das três temáticas declarativas.
O fluxo atual usa DANK e não depende mais do caminho antigo descrito abaixo.

## Goal

Add three declarative themes to the dotfiles theme catalog without changing the
Hyprland/Quickshell architecture or the active theme contract:

1. `nord-quiet-frost` — a Nord-inspired cool, low-noise theme.
2. `glyph-nothing` — a NothingOS-inspired monochrome theme based on the first
   Reddit reference.
3. `aerospace-gruvbox` — a Gruvbox theme based on the Aerospace reference.

Each theme will be a self-contained directory under `themes/` containing a valid
`manifest.json` and one wallpaper asset. Existing semantic palette keys and the
current schema version remain unchanged.

## Visual direction

### Nord — Quiet Frost

Cool blue-gray surfaces, pale text, cyan accent, muted green success state and
warm amber warning state. The panel uses the existing `rail` layout with matte
material and 180 ms transitions. Papirus-Dark and Breeze remain the compatible
defaults.

### Glyph — Nothing-inspired

Near-white/graphite monochrome surfaces with a single red accent, dotted/glyph-like
visual rhythm expressed through the palette and `islands` panel geometry. It uses
solid material, 160 ms transitions, Papirus-Dark for readable icons and Breeze
cursor. No custom widget code or hidden controls are introduced.

### Aerospace — Gruvbox Flight

Dark charcoal surfaces with Gruvbox cream, yellow, orange and olive accents. The
panel uses the compact `architect` layout, matte material and 180 ms transitions,
preserving the dense, tiling-oriented feel of the reference while remaining usable
with the current shell positions.

## Wallpapers and provenance

The implementation will first try to use the original wallpaper assets identified
from each Reddit post. The Aerospace reference attributes its wallpaper as
`spacehawks` by spacegoose, colorized through wallrice.xyz. The Nothing-inspired
post links its wallpaper to Wallhaven `8ggrqy`. If an original file cannot be
retrieved or its reuse terms are unclear, use a visually equivalent asset with a
clear source/license URL and record that provenance in the manifest.

For Nord, use a freely reusable blue/icy wallpaper from a source with a clear
license. Every copied asset must have a SHA-256 recorded in its manifest, matching
the existing repository convention.

## Scope boundaries

- Add only the three theme directories and their assets/manifests.
- Do not change existing themes, panel geometry code, generated-state formats,
  installer behavior, or Plasma configuration.
- Do not add new daemons, widgets, fonts, icon packs or cursor packages.

## Validation

Os passos históricos de validação foram removidos porque o caminho atual não usa
mais o pipeline antigo.
