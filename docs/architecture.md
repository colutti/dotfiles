# Arquitetura

## Configuração e mutações

`hyprland.lua` carrega módulos declarativos para monitores, ambiente, entrada,
workspaces, regras, atalhos, aparência, permissões e autostart. O DANK assume a
camada de shell e os controles de launcher, notificações, clipboard e settings; este
repo fica responsável pelas regras de hardware e da sessão Hyprland.

As regras de monitor continuam sendo a fonte de verdade para esta máquina. O hardware
fica fixo no Hyprland, enquanto o DANK controla a experiência de desktop ao redor.

## Sessão

A entrada de Hyprland inicia o compositor como unidade UWSM. No início da sessão,
`colutti-session-init` publica as variáveis no systemd e D-Bus, limpa helpers de Plasma
que não devem invadir esta sessão e sobe o `dms` como serviço do usuário.

Os portais Hyprland e KDE coexistem: Hyprland atende ScreenCast/ScreenShot; KDE atende
FileChooser e integração Qt.

## Monitores e workspaces

DP-2 usa 3840×2160@60, escala 1.666667, SDR/sRGB/8-bit e VRR off. HDMI-A-1 usa
1920×1080@60, escala 1.25 e posição lógica 384×1296. HDR/10-bit é permitido somente no
DP-2 e sempre retorna a SDR. Os atalhos de workspace, foco e movimento continuam vindo
do Hyprland desta máquina, enquanto o shell visual passa ao DANK.
