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
- `vkcube` selecionou `AMD Radeon RX 7900 XTX (RADV NAVI31)` sob Gamescope e
  MangoHud. O wrapper solicitou GameMode; o perfil próprio mudou para
  performance/DND/inibidor e restaurou balanced/DND off.
- A faixa de jogo apareceu em 772×2139 com 760×20 px, inteiramente dentro do gap
  inferior do HDMI; Telegram e Discord conservaram posição e tamanho.
- Hyprlock criou superfícies 3839×2159 e 1920×1080. Cinco opções antigas foram
  detectadas nos logs, removidas e substituídas pelas opções 0.9.6 válidas; a permissão
  persistente de screencopy foi adicionada para a próxima sessão.
- Duas execuções consecutivas de `session restore` produziram exatamente a mesma
  contagem de clientes, sem duplicatas.
- Janelas adicionais de Zen e Alacritty abriram tiled no workspace 3, sem serem
  sequestradas para 1/2. A janela de configurações da Steam não herdou a geometria da
  janela principal.
- A webcam produziu um quadro MJPEG 1920×1080 e o SoloCast produziu uma amostra PCM
  mono 48 kHz. O receptor Xbox 360 045e:0719 foi enumerado no USB, mas não havia
  gamepad conectado ao subsistema input para testar eventos.
- `gamemoded -t` isolou a falha de otimização: `colutti` ainda não pertence ao grupo
  oficial `gamemode`, exigido pela regra Polkit do pacote. O instalador agora adiciona
  idempotentemente o usuário chamador e o `doctor` verifica essa associação.
- 43 GB de cache antigo do `paru`, 7,7 GiB do `uv` e 3,6 GB do `pip` foram removidos.
  O espaço livre passou de 54 para 91 GiB; jogos, modelos e containers foram preservados.
- DPMS retornou ligado nos dois monitores.
- 40 testes automatizados, parser Lua do Hyprland, `qmllint`, JSON, shell e Python
  passaram na validação final deste checkpoint. O `doctor` terminou apenas com os
  três bloqueios esperados: UWSM inativo, grupo `gamemode` e pacote `swayosd`.

## Pendências bloqueantes para promoção final

1. A sessão atual foi aberta pela entrada simples `Hyprland`, não por
   `Hyprland (uwsm-managed)`. É necessário sair e entrar pela opção correta.
2. O pacote oficial `swayosd` ainda não está instalado e `colutti` ainda precisa entrar
   no grupo `gamemode`; `sudo ./install.sh install` resolve ambos, mas exige
   autenticação administrativa e um novo login.
3. Reboot duplo, Plasma, suspensão/retomada, jogo Proton e compartilhamento de
   tela exigem testes interativos após a nova entrada.

Até esses itens passarem, a sessão é funcional mas não deve ser declarada 100% promovida.
