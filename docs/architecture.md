# Arquitetura

## Configuração e mutações

`hyprland.lua` carrega módulos declarativos para monitores, ambiente, entrada,
workspaces, regras, atalhos, aparência, permissões e autostart. O DANK assume a
camada de shell e os controles de launcher, notificações, clipboard e settings; este
repo fica responsável pelas regras de hardware e da sessão Hyprland.

As regras de monitor continuam sendo a fonte de verdade para esta máquina. O hardware
fica fixo no Hyprland, enquanto o DANK controla a experiência de desktop ao redor.

O DMS fornece o template Matugen oficial para a interface do Zen. O instalador liga esse
arquivo ao `userChrome.css` do perfil Flatpak descoberto em `profiles.ini`, preservando
regras existentes. O template local do Steam gera um skin em `steamui/skins`, sem tocar
nos CSS distribuídos pelo cliente; a seleção do skin é feita uma vez pelo usuário.

## Sessão

A entrada de Hyprland inicia o compositor como unidade UWSM. No início da sessão,
`colutti-session-init` publica as variáveis no systemd e D-Bus, limpa helpers de Plasma
que não devem invadir esta sessão e sobe o `dms` como serviço do usuário.

Os portais Hyprland e KDE coexistem: Hyprland atende ScreenCast/ScreenShot; KDE atende
FileChooser e integração Qt.

## Monitores e workspaces

DP-2 usa 3840×2160@60, escala 1.666667, SDR/8-bit e VRR off. HDMI-A-1 usa
1920×1080@60, escala 1.25, SDR/8-bit e posição lógica 384×1296. `cm_auto_hdr = 2`
permite HDR/10-bit no DP-2 quando um cliente fullscreen compatível o solicita, usando
as primárias EDID, retornando a SDR fora do jogo. Os atalhos de workspace, foco e
movimento continuam vindo do Hyprland desta máquina, enquanto o shell visual passa ao DANK.
