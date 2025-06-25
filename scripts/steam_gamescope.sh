#!/bin/bash

exec ./gamemode.sh

# Verifica se o ambiente não é Hyprland
if [ -z "$HYPRLAND_INSTANCE_SIGNATURE" ]; then
    # Executa o gamescope com os parâmetros especificados
    exec gamescope -W 3840 -H 2160 -f --hdr-enabled --mangoapp -- "$@"
else
    # Executa o comando original se estiver no Hyprland
    exec "$@"
fi