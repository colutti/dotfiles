# Relatório de validação

## Plataforma

Validado em 25 de julho de 2026:

- CachyOS, kernel `7.1.4-1-cachyos`.
- Hyprland `0.56.0-2.1`; Lua validado por `Hyprland --verify-config`.
- Quickshell estável `0.3.0-2.1`; nenhum pacote estrangeiro em `pacman -Qm`.
- Mesa/RADV e Vulkan 64/32-bit `26.1.5`; RX 7900 XTX em `amdgpu`.
- PipeWire `1.6.8` e WirePlumber `0.5.15`.
- Fuzzel `1.14.1`, SwayNC `0.12.6`, Hyprpaper `0.8.4`.
- Backups de inventário e links em
  `~/.local/state/colutti-desktop/backups/`.

## Evidências ao vivo

- DP-2: 3840×2160@60, escala 1.67, posição 0×0.
- HDMI-A-1: 1920×1080@60, escala 1.25, posição 384×1296.
- Barra Quickshell exclusivamente no DP-2.
- Steam em 4/DP-2; Zen em 1; Alacritty em 2; Telegram e Discord tiled em 6.
- Chat medido em 423/1045 px úteis, aproximadamente 28,8%/71,2%.
- Dolphin abriu à direita e com o esquema escuro Studio Ember.
- Os cinco temas geraram hashes diferentes para Fuzzel e SwayNC e terminaram em
  `studio-ember`.
- Seis aplicações consecutivas de tema conservaram o mesmo PID do Hyprpaper; isso
  comprovou a atualização por IPC sem start-limit.
- Fuzzel recebeu `dolphin`, fechou com Escape e não deixou processo.
- Notificação com ação retornou `verified`; crítica permaneceu no histórico; DND
  retornou a `false`.
- Falha induzida do SwayNC acionou Dunst e o timer recuperou SwayNC sem unidade failed.
- HDR mudou apenas DP-2 para `XRGB2101010`/`hdr`; o retorno restaurou
  `XRGB8888`/`srgb`. HDMI e VRR não mudaram.
- `vkcube` selecionou `AMD Radeon RX 7900 XTX (RADV NAVI31)` sob Gamescope,
  MangoHud e GameMode. O perfil mudou para performance/DND/inibidor e restaurou
  balanced/DND off.
- Hyprlock criou superfícies 3839×2159 e 1920×1080; DPMS retornou ligado nos dois
  monitores.
- 40 testes automatizados passaram na última execução intermediária.

## Pendências bloqueantes para promoção final

1. A sessão atual foi aberta pela entrada simples `Hyprland`, não por
   `Hyprland (uwsm-managed)`. É necessário sair e entrar pela opção correta.
2. O pacote oficial `swayosd` ainda não está instalado; a instalação exige autenticação
   administrativa.
3. Reboot duplo, Plasma, suspensão/retomada, jogo Proton, webcam e compartilhamento de
   tela exigem testes interativos após a nova entrada.

Até esses itens passarem, a sessão é funcional mas não deve ser declarada 100% promovida.
