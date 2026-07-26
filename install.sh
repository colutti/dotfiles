#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
backup_root="${XDG_STATE_HOME:-${HOME}/.local/state}/colutti-desktop/backups"
mode="${1:-help}"
config_packages=(hyprland systemd uwsm alacritty xdg-desktop-portal autostart gtk vscodium)

usage() {
  printf '%s\n' \
    "usage: ./install.sh <preflight|install|link|validate|rollback|doctor>" \
    "  preflight  collect a read-only hardware and software report" \
    "  install    install official repository packages with pacman" \
    "  link       back up existing files and stow the configuration" \
    "  validate   run repository, Hyprland and systemd checks" \
    "  rollback   restore the most recent link backup" \
    "  doctor     run dms doctor"
}

packages() {
  python -c 'import json,sys; print(*json.load(open(sys.argv[1]))["install"])' \
    "${repo_root}/packages.json"
}

preflight() {
  local stamp report_dir
  stamp="$(date -u +%Y%m%dT%H%M%S%NZ)"
  report_dir="${backup_root}/${stamp}/inventory"
  mkdir -p "${report_dir}"
  uname -a >"${report_dir}/kernel.txt"
  pacman -Qqe >"${report_dir}/packages-explicit.txt"
  pacman -Qm >"${report_dir}/packages-foreign.txt" || true
  lspci -nnk >"${report_dir}/pci.txt"
  lsusb >"${report_dir}/usb.txt"
  systemctl --user list-unit-files >"${report_dir}/user-units.txt"
  wpctl status >"${report_dir}/pipewire.txt" 2>&1 || true
  # KScreen can wait indefinitely for the Plasma KScreen service under Hyprland;
  # preflight is read-only and must never hold the whole audit open.
  if ! timeout 5s kscreen-doctor -o >"${report_dir}/kscreen.txt" 2>&1; then
    printf 'kscreen-doctor unavailable or timed out under this session\n' \
      >>"${report_dir}/kscreen.txt"
  fi
  git -C "${repo_root}" status --short --branch >"${report_dir}/git.txt"
  printf 'inventory=%s\n' "${report_dir}"
}

install_packages() {
  local desktop_user
  if (( EUID != 0 )); then
    printf 'install must run as root: sudo ./install.sh install\n' >&2
    exit 1
  fi
  if snapper -c root list >/dev/null 2>&1; then
    snapper -c root create --type single \
      --description "Before Colutti Hyprland workstation install"
  fi
  mapfile -t official < <(packages | tr ' ' '\n')
  pacman -Syu --needed -- "${official[@]}"
  desktop_user="${SUDO_USER:-}"
  if [[ -n "${desktop_user}" && "${desktop_user}" != root ]] &&
    getent group gamemode >/dev/null &&
    ! id -nG "${desktop_user}" | tr ' ' '\n' | grep -qx gamemode; then
    usermod -aG gamemode -- "${desktop_user}"
    printf 'Added %s to gamemode; log in again before testing GameMode.\n' \
      "${desktop_user}"
  fi
}

link_config() {
  local stamp target marker relink=false
  stamp="$(date -u +%Y%m%dT%H%M%S%NZ)"
  if [[ -L "${HOME}/.config/hypr/hyprland.lua" ]] &&
    [[ "$(readlink -f -- "${HOME}/.config/hypr/hyprland.lua")" == \
      "${repo_root}/hyprland/.config/hypr/hyprland.lua" ]]; then
    marker="$(find "${backup_root}" -mindepth 2 -maxdepth 2 -type f -name link-complete \
      -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
    if [[ -n "${marker}" ]]; then
      target="$(dirname "${marker}")/home"
      relink=true
    fi
  fi
  target="${target:-${backup_root}/${stamp}/home}"
  mkdir -p "${target}"
  for path in \
    .config/hypr \
    .config/systemd/user \
    .config/uwsm \
    .config/alacritty \
    .config/xdg-desktop-portal \
    .config/autostart \
    .config/gtk-3.0 \
    .config/gtk-4.0 \
    .config/Kvantum \
    .config/VSCodium/User \
    .zen; do
    if [[ -e "${HOME}/${path}" && ! -L "${HOME}/${path}" &&
          ! -e "${target}/${path}" ]]; then
      mkdir -p "${target}/$(dirname "${path}")"
      cp -a -- "${HOME}/${path}" "${target}/${path}"
    fi
  done

  local package source relative destination saved
  for package in "${config_packages[@]}"; do
    while IFS= read -r -d '' source; do
      relative="${source#"${repo_root}/${package}/"}"
      destination="${HOME}/${relative}"
      if [[ -e "${destination}" || -L "${destination}" ]]; then
        if [[ "$(readlink -f -- "${destination}")" == "$(readlink -f -- "${source}")" ]]; then
          continue
        fi
        saved="${target}/${relative}"
        if [[ ! -e "${saved}" && ! -L "${saved}" ]]; then
          mkdir -p "$(dirname "${saved}")"
          cp -a -- "${destination}" "${saved}"
        fi
        rm -f -- "${destination}"
      fi
    done < <(find "${repo_root}/${package}" \( -type f -o -type l \) -print0)
  done

  stow --dir="${repo_root}" --target="${HOME}" --restow --no-folding \
    "${config_packages[@]}"
  systemctl --user daemon-reload 2>/dev/null || true
  mkdir -p "${HOME}/.local/bin"
  ln -sfn "${repo_root}/scripts/session-init" \
    "${HOME}/.local/bin/colutti-session-init"
  ln -sfn "${repo_root}/scripts/session-logout" \
    "${HOME}/.local/bin/colutti-session-logout"
  mkdir -p "${XDG_CONFIG_HOME:-${HOME}/.config}/colutti-desktop"
  if [[ ! -e "${XDG_CONFIG_HOME:-${HOME}/.config}/colutti-desktop/settings.json" ]]; then
    cp -- "${repo_root}/settings/default.json" \
      "${XDG_CONFIG_HOME:-${HOME}/.config}/colutti-desktop/settings.json"
  fi
  if [[ "${relink}" == false ]]; then
    : >"${backup_root}/${stamp}/link-complete"
  fi
  printf 'backup=%s\n' "${target}"
}

validate() {
  python -m json.tool "${repo_root}/settings/default.json" >/dev/null
  find "${repo_root}/themes" -name manifest.json -exec python -m json.tool {} \; >/dev/null
  if command -v Hyprland >/dev/null; then
    Hyprland --verify-config -c "${repo_root}/hyprland/.config/hypr/hyprland.lua"
  fi
  if command -v systemd-analyze >/dev/null; then
    local verify_output verify_status
    set +e
    verify_output="$(
      find "${repo_root}/systemd/.config/systemd/user" -type f \
        \( -name '*.service' -o -name '*.target' \) -print0 |
        xargs -0r systemd-analyze --user verify 2>&1
    )"
    verify_status=$?
    set -e
    printf '%s\n' "${verify_output}"
    if (( verify_status != 0 )) &&
      printf '%s\n' "${verify_output}" |
        grep -Ev 'Command .+ is not executable: No such file or directory|^$' |
        grep -q .; then
      return "${verify_status}"
    fi
  fi
}

rollback() {
  local latest marker
  marker="$(find "${backup_root}" -mindepth 2 -maxdepth 2 -type f -name link-complete \
    -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
  [[ -n "${marker}" ]] || { printf 'no completed link backup available\n' >&2; exit 1; }
  latest="$(dirname "${marker}")/home"
  stow --dir="${repo_root}" --target="${HOME}" --delete "${config_packages[@]}" || true
  cp -a -- "${latest}/." "${HOME}/"
  printf 'restored=%s\n' "${latest}"
}

case "${mode}" in
  preflight) preflight ;;
  install) install_packages ;;
  link) link_config ;;
  validate) validate ;;
  rollback) rollback ;;
  doctor) exec dms doctor ;;
  help|-h|--help) usage ;;
  *) usage >&2; exit 64 ;;
esac
