#!/bin/bash

# Lista de pacotes para instalar (pode editar facilmente)
PACKAGES=(
  stow
  xdg-desktop-portal-hyprland
  xdg-desktop-portal-wlr
  jq
  dms-git
  kitty
  steam
  telegram-desktop
  discord
  firefox
  gamemode
  mangohud
  codium
)

# Instala todos os pacotes necessários
paru -S --needed --noconfirm "${PACKAGES[@]}"

# Aplica todos os dotfiles usando Stow, removendo antes para garantir sobrescrita
cd ~/dotfiles
for pkg in *; do
  stow -D $pkg   # Remove symlinks/arquivos existentes
  stow $pkg      # Cria novos symlinks
done

echo "Instalação e configuração dos dotfiles concluída!"