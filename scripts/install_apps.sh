#!/bin/bash

# --- FUNÇÕES AUXILIARES ---
# Função para instalar pacotes via pacman (repositórios oficiais)
install_pacman() {
    echo "Instalando pacotes dos repositórios oficiais: $*"
    # --needed: evita reinstalar pacotes já atualizados
    # --noconfirm: assume 'sim' para todas as perguntas
    sudo pacman -S --noconfirm --needed "$@" || { echo "Erro ao instalar pacotes do pacman: $*"; exit 1; }
}

# Função para instalar pacotes via yay (AUR)
install_yay_app() {
    echo "Instalando pacotes do AUR: $*"
    # --needed: evita reinstalar pacotes já atualizados
    # --noconfirm: assume 'sim' para todas as perguntas
    yay -S --noconfirm --needed "$@" || { echo "Erro ao instalar pacotes do AUR: $*"; exit 1; }
}

# Função para instalar Flatpak apps
install_flatpak_app() {
    echo "Instalando Flatpak: $*"
    flatpak install --or-update --assumeyes flathub "$@" || { echo "Erro ao instalar Flatpak: $*"; exit 1; }
}

# --- INÍCIO DO SCRIPT ---

echo "--- Iniciando a instalação completa para o ambiente Hyprland ---"

# 1. Instalar yay (se não estiver instalado)
echo "Verificando e instalando yay..."
if ! command -v yay &> /dev/null; then
    echo "yay não encontrado. Instalando..."
    install_pacman git base-devel
    git clone https://aur.archlinux.org/yay.git || { echo "Erro ao clonar repositório do yay"; exit 1; }
    (cd yay && makepkg -si --noconfirm) || { echo "Erro ao construir e instalar yay"; exit 1; }
    rm -rf yay # Limpa o diretório de construção do yay
    echo "yay instalado com sucesso!"
else
    echo "yay já está instalado."
fi

# 2. Atualizar o Sistema Primeiro (agora que o yay está disponível)
echo "Atualizando o sistema e o cache de pacotes com yay..."
yay -Syu --noconfirm || { echo "Erro ao atualizar o sistema. Verifique sua conexão e repositórios."; exit 1; }

# 3. Instalar Programas do Repositório Oficial (pacman)
echo "Instalando pacotes essenciais do pacman..."
install_pacman \
    hyprland \
    kitty \
    dolphin \
    wofi \
    pipewire \
    pipewire-pulse \
    brightnessctl \
    playerctl \
    networkmanager \
    network-manager-applet \
    udiskie \
    gnome-keyring \
    dbus \
    polkit \
    polkit-gnome \
    xdg-desktop-portal-hyprland \
    xdg-desktop-portal-kde \
    xdg-desktop-portal-gnome \
    gamemode \
    mesa \
    vulkan-radeon \
    lib32-mesa \
    lib32-vulkan-radeon \
    wpctl \
    qt5ct \
    steam

# 4. Instalar Programas do AUR (yay)
echo "Instalando pacotes do AUR (isso pode demorar mais)..."
install_yay_app \
    hyprlock \
    wlogout \
    hyprshot \
    waybar \
    hypridle \
    swaync \
    hyprpaper \
    gamescope \
    vesktop-bin \
    telegram-desktop \
    qt6ct-kde \
    nwg-displays \
    vscodium-bin \
    waypaper

# 5. Configurar Flatpak e Instalar Aplicativos Flatpak
echo "Configurando Flatpak e instalando aplicativos Flatpak..."
install_pacman flatpak # Garante que flatpak esteja instalado antes de usá-lo
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpak.org/repo/flathub.flatpakrepo || { echo "Erro ao adicionar repositório Flathub"; exit 1; }

install_flatpak_app app.zen_browser.zen # Zen Browser via Flatpak

# 6. Configurações Pós-Instalação para Gamescope
echo "Aplicando configurações específicas para Gamescope..."
# Configurar permissões CAP_SYS_NICE para gamescope (para otimizações de jogos)
sudo setcap 'cap_sys_nice=+ep' /usr/bin/gamescope || { echo "Aviso: Erro ao configurar CAP_SYS_NICE para gamescope. Verifique se gamescope está corretamente instalado."; }