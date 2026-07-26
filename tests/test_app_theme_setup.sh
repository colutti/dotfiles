#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
fixture_root="$(mktemp -d)"
trap 'rm -rf -- "$fixture_root"' EXIT

grep -Fq '[templates.steam]' "$repo_root/matugen/.config/matugen/config.toml"
grep -Fq 'steamui/skins/colutti-matugen/libraryroot.custom.css' \
  "$repo_root/matugen/.config/matugen/config.toml"
grep -Fq '[templates.zen]' "$repo_root/matugen/.config/matugen/config.toml"
grep -Fq '.var/app/app.zen_browser.zen/.zen/colutti-dms-zen.css' \
  "$repo_root/matugen/.config/matugen/config.toml"
! grep -Fq '/steamui/css/' \
  "$repo_root/matugen/.config/matugen/templates/steam-libraryroot.custom.css"

zen_root="$fixture_root/.var/app/app.zen_browser.zen/.zen"
profile_dir="$zen_root/profile.Install"
steam_root="$fixture_root/.local/share/Steam"
mkdir -p "$profile_dir/chrome" "$zen_root/profile.Default" "$steam_root/steamui/css"
cat >"$zen_root/profiles.ini" <<'EOF'
[Profile0]
Name=Default
IsRelative=1
Path=profile.Default
Default=1

[General]
StartWithLastProfile=1
Version=2

[Install123]
Default=profile.Install
EOF
printf '/* user-owned Zen rules */\n' >"$profile_dir/chrome/userChrome.css"
printf '/* vendor CSS must remain untouched */\n' >"$steam_root/steamui/css/library.css"

HOME="$fixture_root" \
COLUTTI_ZEN_ROOT="$zen_root" \
COLUTTI_DMS_ZEN_CSS="$zen_root/colutti-dms-zen.css" \
  "$repo_root/scripts/setup-zen-matugen"

user_chrome="$profile_dir/chrome/userChrome.css"
user_js="$profile_dir/user.js"
grep -Fq '/* BEGIN COLUTTI DMS MATUGEN */' "$user_chrome"
grep -Fq '@import url("file://' "$user_chrome"
grep -Fq '/* END COLUTTI DMS MATUGEN */' "$user_chrome"
grep -Fq 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);' "$user_js"
grep -Fq 'user-owned Zen rules' "$user_chrome"

before_hash="$(sha256sum "$user_chrome" "$user_js")"
HOME="$fixture_root" \
COLUTTI_ZEN_ROOT="$zen_root" \
COLUTTI_DMS_ZEN_CSS="$zen_root/colutti-dms-zen.css" \
  "$repo_root/scripts/setup-zen-matugen"
after_hash="$(sha256sum "$user_chrome" "$user_js")"
[[ "$before_hash" == "$after_hash" ]]

[[ ! -e "$steam_root/steamui/skins/colutti-matugen/libraryroot.custom.css" ]]
cmp -s "$steam_root/steamui/css/library.css" <(printf '/* vendor CSS must remain untouched */\n')

missing_root="$fixture_root/missing-zen"
HOME="$fixture_root" COLUTTI_ZEN_ROOT="$missing_root" \
  "$repo_root/scripts/setup-zen-matugen" 2>"$fixture_root/missing.log"
grep -Fq 'Zen profile not found' "$fixture_root/missing.log"

printf 'PASS: Zen profile wiring is preserved and idempotent\n'
