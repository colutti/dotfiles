# Steam HDR Gaming Design

**Date:** 2026-08-09

**Goal:** Make DP-2 use permanent 4K HDR at 10-bit while providing a safe, reproducible Steam launch path for native-resolution HDR games through Gamescope with a readable MangoHud overlay and temporary CachyOS performance profile.

**Scope:** DP-2 only. Keep its 3840x2160@60 mode and VRR disabled; retain HDMI-A-1 as SDR/8-bit. Preserve Plasma fallback, existing session behavior, and a documented SDR recovery route. Do not install non-official packages, launch Steam/games, or enable Gamescope as the entire login session.

## Architecture

The persisted monitor source of truth is the declarative Hyprland monitor module: DP-2 will be changed to 10-bit HDR, while its mode, location, scale, and VRR policy stay unchanged. The desktop monitor mutation boundary must be restored before a live monitor change is attempted. It will read typed settings, atomically render the generated monitor configuration, apply the requested DP-2 HDR change, and hold a 20-second confirmation transaction that restores the last known-good monitor state if it is not confirmed.

MangoHud configuration belongs in a tracked dotfiles path and is linked into `~/.config/MangoHud/MangoHud.conf`. It reports GPU/CPU temperatures and power, VRAM/RAM, FPS and frame-time percentiles, HDR status, refresh rate, renderer, and the active performance profile. Gamescope must use `--mangoapp`; ordinary `mangohud` wrapping is intentionally not combined with Gamescope.

Steam launch options will remain per game. The standard HDR native-resolution wrapper is:

```bash
DXVK_HDR=1 game-performance gamescope -f -W 3840 -H 2160 -w 3840 -h 2160 --hdr-enabled --mangoapp -- %command%
```

The matching game must use an HDR-capable Proton version and enable HDR in its own settings. The command deliberately omits Gamescope scaling flags, inverse tone mapping, VRR and frame-rate limiting: output and nested resolutions are both 4K, HDR is native rather than SDR-to-HDR conversion, the display has no VRR, and its maximum refresh is 60 Hz.

## Components and responsibilities

- `hyprland/.config/hypr/modules/monitors.lua` declares permanent DP-2 HDR/10-bit hardware policy.
- `settings/default.json` declares the same monitor policy for typed settings and generated output.
- `desktopctl/colutti_desktopctl.py` and `bin/colutti-desktopctl` restore the required safe mutation boundary. They validate settings and restrict HDR to DP-2.
- `mangohud/.config/MangoHud/MangoHud.conf` is the global performance overlay configuration.
- `packages.json` declares every executable used by the persistent configuration, including `goverlay` only if the tracked setup relies on its GUI.
- `docs/hardware.md`, `docs/architecture.md`, `docs/recovery.md`, and `README.md` document permanent HDR, known capture constraints, the recovery route, and the exact Steam command.

## Safety and recovery

The live monitor operation must never change HDMI-A-1, VRR, geometry, scale, or mode. It must save the preceding settings and generated monitor state before application. If visual confirmation is not received within 20 seconds, it restores that state automatically. Recovery remains possible by selecting Plasma at login, or by using the documented desktop recovery command from a TTY.

HDR remains active after a confirmed transaction and after future Hyprland restarts. SDR is not reapplied after a game closes. The known drawback is that screen capture and screen sharing may be limited by HDR/10-bit.

## Validation

Validation has three tiers:

1. Offline: JSON parsing, Python compilation/tests for settings validation and transaction behavior, `Hyprland --verify-config`, and `./install.sh validate`.
2. Live reversible: inspect the HDR transaction request, confirm only DP-2 reaches `XRGB2101010`/HDR, and confirm timeout restores the previous state.
3. User-observed: user confirms the DP-2 HDR image during the 20-second window; no game is automatically launched. Steam game HDR and MangoHud status are then tested manually with the supplied launch option.
