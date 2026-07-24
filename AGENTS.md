# Colutti desktop agent guide

## Architecture

- `hyprland/.config/hypr/hyprland.lua` is the only Hyprland entrypoint.
- `hyprland/.config/hypr/modules/` contains declarative Lua modules. Do not let the
  settings GUI edit them.
- `desktopctl/colutti_desktopctl.py` is the mutation boundary. Settings are typed JSON;
  generated files are replaced atomically under
  `~/.local/state/colutti-desktop/generated/`.
- `quickshell/.config/quickshell/colutti/` owns only the primary-monitor bar.
- Fuzzel owns the launcher. SwayNC owns notifications and the control center.
- `systemd/.config/systemd/user/` owns all session daemons. Do not add daemon processes
  to Hyprland autostart.
- Plasma is a fallback and must remain installed and selectable.

## Invariants

1. Official CachyOS/Arch repositories only. Never add an AUR helper or `*-git` package.
2. Never run two notification daemons. Dunst is emergency fallback only.
3. Monitor changes require a 20-second confirmation transaction.
4. App restoration must check existing clients and use one-shot exec rules.
5. No arbitrary startup sleeps. Poll a socket or order through systemd.
6. Default desktop is SDR, 8-bit and VRR off. HDR automation is restricted to DP-2.
7. The login entry must be `Hyprland (uwsm-managed)` before final promotion.

## Safe commands

```bash
./tests/run
Hyprland --verify-config -c "$PWD/hyprland/.config/hypr/hyprland.lua"
qmllint quickshell/.config/quickshell/colutti/shell.qml
./install.sh preflight
./install.sh validate
./install.sh doctor
```

`install`, `link`, reboot, session logout and rollback change machine state. Read
`docs/recovery.md` first.
