# Clean Arch Workstation Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an idempotent `./install.sh bootstrap` command that rebuilds the current `colutti` Arch workstation from a clean base installation.

**Architecture:** Keep `install.sh` as the user-facing orchestration boundary and move package/profile/service helpers into focused shell scripts under `scripts/`. Extend `packages.json` with explicit package groups and hardware profiles. The bootstrap runs as the normal user, uses `sudo` only for pacman/system operations, links the existing configuration, installs Zen via Flatpak, and validates without adding a permanent test suite.

**Tech Stack:** Bash, pacman, Flatpak, systemd, Podman, JSON, Hyprland/UWSM.

---

### Task 1: Reconcile the package manifest

**Files:**
- Modify: `packages.json`
- Modify: `install.sh`

- [ ] Add grouped package lists for base tools, Hyprland/UWSM, DANK/session, minimal KDE integration, media/desktop utilities, AMD graphics, gaming, and applications.
- [ ] Include every executable referenced by tracked configs and session scripts, including Dolphin, Quickshell, SwayNC, Fuzzel, Hyprpaper, Hypridle, Hyprsunset, SwayOSD, PipeWire/WirePlumber, VSCodium, and the existing apps.
- [ ] Include official AMD Mesa/Vulkan 64-bit and 32-bit packages for the RX 7900 XTX profile.
- [ ] Keep optional packages separate and do not remove packages already installed.
- [ ] Make package extraction work with the grouped JSON while retaining compatibility with the existing `install` list.

### Task 2: Implement bootstrap orchestration

**Files:**
- Modify: `install.sh`
- Create: `scripts/bootstrap`
- Create: `scripts/hardware-profile`

- [ ] Add `bootstrap` and `bootstrap --dry-run` modes.
- [ ] Verify the current user is `colutti`, the system is Arch/CachyOS, sudo and network are available, and the repository is complete.
- [ ] Detect the AMD/Navi31 hardware profile and produce a readable report without making hardware mutations.
- [ ] Resolve the grouped package list and install it through `sudo pacman -Syu --needed`.
- [ ] Keep package installation idempotent and fail with actionable messages when prerequisites are missing.
- [ ] In dry-run mode, do not change packages, files, services, Flatpak state, or user configuration.

### Task 3: Configure system and user services

**Files:**
- Modify: `install.sh`
- Modify: `packages.json`
- Create: `scripts/bootstrap-services`

- [ ] Enable NetworkManager, power-profiles-daemon, and GameMode only when their units exist.
- [ ] Install the user session units through the existing link flow without starting graphical daemons outside Hyprland.
- [ ] Preserve the single-notification-daemon invariant and Plasma fallback.
- [ ] Install/verify the UWSM Hyprland desktop entry and document the required login selection.
- [ ] Ensure PipeWire/WirePlumber and portal packages are present without requiring a running graphical session during bootstrap.

### Task 4: Make linking and application setup clean-install safe

**Files:**
- Modify: `install.sh`
- Modify: `scripts/setup-zen-matugen`
- Modify: `README.md`

- [ ] Ensure all tracked active configuration packages are linked, including current DANK/Hyprland, application, portal, theme, and service configuration.
- [ ] Preserve existing backups and rollback behavior.
- [ ] Install Zen from Flathub using `app.zen_browser.zen`, then configure its Matugen profile wiring.
- [ ] Create required local-bin and generated-state directories.
- [ ] Keep personal account data out of the bootstrap.
- [ ] Document the exact clone/bootstrap command, installed components, minimal KDE scope, hardware profile, first-login actions, dry-run, recovery, and validation limitations.

### Task 5: Validate in clean and current environments

**Files:**
- Create: `scripts/bootstrap-container-check`
- Modify: `README.md`

- [ ] Run shell syntax checks, JSON parsing, Hyprland verification, and systemd unit verification.
- [ ] Run a disposable Arch Podman container check that clones/copies the repository, resolves the package manifest, and executes bootstrap dry-run without mutating the host.
- [ ] Run bootstrap dry-run on the current machine and inspect the generated report.
- [ ] Verify the real machine package/profile/service state without rebooting, logging out, launching games, or changing monitor configuration.
- [ ] Report exactly which graphical and hardware behaviors remain unobservable from the container.

