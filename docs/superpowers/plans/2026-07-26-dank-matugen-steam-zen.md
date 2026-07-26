# DANK Matugen Steam and Zen Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make DANK/Matugen theme changes regenerate a Steam skin and apply the existing DMS Zen theme output to the user's Zen UI on the next launch.

**Architecture:** Reuse DMS's packaged Zen Matugen detector/template and add a repository-owned user Matugen template for Steam's supported `steamui/skins` mechanism. Add a small idempotent setup script that discovers the Flatpak Zen profile, enables `userChrome.css`, and imports DMS's generated `zen.css` without overwriting existing profile CSS. Steam remains opt-in through its Interface skin selector; no running app is restarted and no vendor CSS is modified.

**Tech Stack:** Bash, Matugen 4.x/DMS 1.5.x TOML templates, Zen `userChrome.css`, Steam Homebrew skin CSS, targeted validation.

---

### Task 1: Add the Steam Matugen template

**Files:**
- Modify: `matugen/.config/matugen/config.toml`
- Create: `matugen/.config/matugen/templates/steam-libraryroot.custom.css`

- [x] **Step 1: Add a user template registration**

Add a `steam` template entry using the same absolute-home convention already used by the Telegram template, with output path `/home/colutti/.local/share/Steam/steamui/skins/colutti-matugen/libraryroot.custom.css`.

- [x] **Step 2: Write the Steam skin CSS**

Use Matugen semantic colors for Steam's library/client surfaces, primary text, muted text, outline, accent, selected states, buttons, and badges. Keep selectors scoped to Steam's current library/client DOM and avoid JavaScript or modifications to files under `steamui/css`.

- [x] **Step 3: Validate the template syntax**

Run `matugen --dry-run --config "$PWD/matugen/.config/matugen/config.toml" color hex '#282828'` and confirm it exits successfully without changing the user's Steam files.

### Task 2: Connect DMS's generated Zen CSS to the profile

**Files:**
- Create: `scripts/setup-zen-matugen`
- Modify: `install.sh`

- [x] **Step 1: Implement profile discovery and idempotent wiring**

Discover `~/.var/app/app.zen_browser.zen/.zen/profiles.ini`, select the `Default=1` profile or the install `Default=` entry, resolve relative paths, create `chrome/`, preserve existing `userChrome.css`, and add only a clearly delimited managed import block pointing to `~/.config/DankMaterialShell/zen.css`. Add the preference to `user.js` only when absent. Never edit `zen-themes.css` or `userContent.css`.

- [x] **Step 2: Integrate setup into the safe link flow**

Call the script from `install.sh link` after configuration links are established. Keep failure non-fatal when Zen is not installed, while returning an error for malformed profile metadata or unsafe paths.

### Task 3: Make Steam's target directory available and document first activation

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture.md`

- [x] **Step 1: Document the one-time Steam action**

Explain that the generated skin is at `~/.local/share/Steam/steamui/skins/colutti-matugen/` and must be selected once under Steam Settings → Interface; subsequent DANK theme changes only regenerate the CSS for the next Steam launch.

### Task 4: Verify the real DMS/Matugen path without restarting apps

**Files:**
- No source changes.

- [x] **Step 1: Validate repository files**

Run `bash -n scripts/setup-zen-matugen install.sh` and `./install.sh validate`.

- [x] **Step 2: Generate with the installed Matugen path**

Use `dms matugen generate --kind hex --value '#282828' --run-user-templates` only after confirming Steam is not running; verify the generated Steam CSS exists, contains the current generated colors, and `~/.config/DankMaterialShell/zen.css` is present. Do not restart Steam or Zen.

- [x] **Step 3: Confirm the live wiring**

Inspect `profiles.ini`, `userChrome.css`, `user.js`, and the Steam skin path. Report that application rendering still requires closing/reopening each app, consistent with the requested next-launch behavior.
