#!/bin/bash

# Lista de pacotes para instalar (pode editar facilmente)
PACKAGES=(
  ags-hyprpanel-git
  aylurs-gtk-shell-git
  bluez
  bluez-utils
  brightnessctl
  btop
  cargo
  codium
  dart-sass
  discord
  firefox
  gamemode
  grimblast-git
  gvfs
  gtksourceview3
  hyprland
  hyprpicker
  hyprsunset-git
  jq
  kitty
  lazydocker
  lazygit
  libgtop
  libsoup3
  mangohud
  matugen-bin
  networkmanager
  nodejs
  nvim
  pacman-contrib
  power-profiles-daemon
  python
  python-gpustat
  pywal-git
  steam
  stow
  swww
  telegram-desktop
  terminus-font
  upower
  wf-recorder-git
  wireplumber
  wl-clipboard
  xdg-desktop-portal
  xdg-desktop-portal-gtk
  xdg-desktop-portal-hyprland
  xdg-desktop-portal-wlr
  lm_sensors
  yazi
  hypridle
  hyprlock
  qt5-wayland
  qt6-wayland
  ttf-liberation
  noto-fontr
  noto-fonts-emoji
  ttf-carlito
  ttf-caladea
  ttf-ms-fonts
  walker
  elephant
  elephant-desktopapplications
  github-cli
  ly
)
# Instala todos os pacotes necessários
paru -S --needed --noconfirm "${PACKAGES[@]}"

echo "Instalação e configuração dos dotfiles concluída!"

systemctl enable ly.service
