# Arquitetura

## Configuração e mutações

`hyprland.lua` carrega módulos declarativos para monitores, ambiente, entrada,
workspaces, regras, atalhos, aparência, permissões e autostart. A GUI nunca escreve
nesses módulos. Ela chama `colutti-desktopctl`, que valida `settings.json`, produz uma
geração temporária e publica o conjunto completo atomicamente.

Temas verificam o SHA-256 do wallpaper antes da publicação. A geração inclui Hyprland,
Hyprpaper, Hyprlock, Quickshell, Fuzzel, SwayNC, GTK, KDE/Qt, Alacritty e a extensão
local do VSCodium. O Zen segue a preferência claro/escuro do portal. Hyprpaper recebe
wallpapers novos por IPC, evitando reinícios em sequência.

Mudanças de monitor capturam primeiro o estado vivo. Uma falha parcial ou a ausência de
confirmação em 20 segundos restaura geometria e `settings.json`.

## Sessão

A entrada **Hyprland (uwsm-managed)** inicia o compositor como unidade UWSM. No evento
de início, `colutti-session-init` publica as variáveis Wayland no systemd e D-Bus,
reinicia os portais na ordem correta e ativa `colutti-desktop.target`.

O target ordena Quickshell, SwayNC, Hyprpaper, Hypridle, Hyprsunset, clipboard e o agente
Polkit KDE. O restaurador espera o socket e os workspaces, verifica processos e clientes
existentes e aplica propriedades one-shot somente às instâncias que acabou de criar.

Fuzzel é o launcher. SwayNC é o único servidor principal de notificações e fornece
histórico, ações, DND, mídia, volume e controles. Se ele falhar, Dunst assume
temporariamente; um timer tenta recuperar SwayNC, e os dois serviços possuem conflito
explícito. Quickshell mantém somente a barra do DP-2 e o tray.

Os portais Hyprland e KDE coexistem: Hyprland atende ScreenCast/ScreenShot; KDE atende
FileChooser e integração Qt.

## Monitores e workspaces

DP-2 usa 3840×2160@60, escala 1.666667, SDR/sRGB/8-bit e VRR off. HDMI-A-1 usa
1920×1080@60, escala 1.25 e posição lógica 384×1296. HDR/10-bit é permitido somente no
DP-2 e sempre retorna a SDR.

DP-2: 1 Web, 2 Code, 3 Media, 4 Games, 5 Focus. HDMI-A-1: 6 Chat, 7 Music, 8 Monitor.
O workspace 6 permanece visível enquanto o monitor superior alterna.
