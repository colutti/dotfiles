# Clean Arch Workstation Bootstrap Design

**Date:** 2026-07-26

**Goal:** Rebuild the current `colutti` Arch workstation from a clean base installation with one documented, idempotent command while preserving the current Hyprland/DANK behavior and hardware-specific configuration.

**Scope:** Restore operating-system packages, desktop components, applications, services, configuration links, themes, portals, gaming dependencies, and the UWSM session. Do not restore application accounts, authentication tokens, chat history, Steam libraries, browser data, or other personal data.

## Architecture

The repository will expose one user-facing command:

```bash
./install.sh bootstrap
```

The command runs as `colutti`, elevates only package and system-service operations through `sudo`, and performs these phases in order:

1. Verify Arch/CachyOS, user identity, network, `sudo`, repository state, and required base commands.
2. Detect the machine profile from PCI, CPU, audio, and display information.
3. Install official Arch/CachyOS repository packages with `pacman --needed`.
4. Install the Zen Flatpak from Flathub using the existing application ID.
5. Enable required system services without installing a full KDE desktop.
6. Link repository configuration with the existing backup and rollback mechanism.
7. Install or enable the `Hyprland (uwsm-managed)` session entry and user units.
8. Configure Matugen, Zen, Steam, themes, and generated state.
9. Run targeted validation and print manual post-install actions.

The existing `preflight`, `install`, `link`, `validate`, `rollback`, and `doctor` modes remain available for recovery and advanced use. `bootstrap` composes them with explicit checks and safe failure behavior.

## Package policy

Only official Arch or CachyOS repositories and Flathub are allowed. No AUR helper, AUR package, or `*-git` package is introduced.

Packages are grouped in `packages.json` by responsibility:

- base tools and fonts;
- Hyprland/UWSM/session infrastructure;
- DANK, portals, Qt/KDE integration, and the minimal Dolphin/FileChooser stack;
- audio, brightness, clipboard, screenshots, notification, and media services;
- AMD graphics and 32-bit Vulkan support for the RX 7900 XTX;
- Steam, Discord, Telegram, gamescope, MangoHud, and GameMode;
- optional packages that are never installed by default.

`pacman --needed` is used for every package transaction. Existing packages are not removed and already-installed packages are not reinstalled. Hardware detection adds only packages required by the detected profile; the current AMD profile is the default target for this machine.

## Repository cleanup

Before implementation, the configuration inventory will be reconciled against active references and services. Cleanup is limited to files that are demonstrably unused or contradictory. It may reorganize package manifests and installer functions, remove stale test artifacts and obsolete documentation instructions, and remove unused Kitty or duplicate legacy configuration only after reference checks. It must preserve the current recovery path, Plasma availability, DANK configuration, Hyprland modules, application configs that are actively restored, and emergency notification fallback.

No permanent test suite will be added. Repository checks are operational validations: shell syntax, JSON parsing, package-resolution simulation, Hyprland config verification, systemd unit verification, link inspection, and service/package state checks.

## Clean-environment validation

The bootstrap will support a non-mutating `--dry-run` or equivalent simulation for package resolution and phase reporting. A disposable Arch container run by Podman will validate repository checkout, package manifest resolution, shell syntax, dry-run behavior, and configuration validation that does not require a live compositor.

The container cannot prove GPU acceleration, monitor geometry, PipeWire device selection, UWSM login behavior, or real application rendering. Those limitations will be reported explicitly. The real machine validation will verify the AMD driver, Vulkan libraries, monitor rules, user units, portals, and final `install.sh doctor` output without launching games or rebooting automatically.

## Documentation

`README.md` will become the complete recovery guide. It will document:

- prerequisites for a clean Arch installation;
- the exact clone and bootstrap commands;
- what `bootstrap` installs and configures;
- the minimal KDE components and why they are present;
- hardware-specific AMD/monitor behavior;
- what is intentionally not restored;
- dry-run and recovery commands;
- first-login actions for Steam, Discord, Telegram, Zen, and the UWSM session;
- validation output and known limits.

The implementation plan will identify exact files and commands for each phase. No network credentials or application secrets will be stored in the repository.

