# Sessão controlada

Estado em 25 de julho de 2026. Itens marcados foram comprovados nesta sessão; itens
restantes exigem nova entrada, credencial, hardware ou interação humana real.

- [x] Modos, escalas, posições, SDR/8-bit e VRR off via `hyprctl monitors -j`.
- [x] Geometria e tiling de Zen, Alacritty, Steam, Telegram e Discord.
- [ ] Duas entradas consecutivas pela sessão **Hyprland (uwsm-managed)** sem duplicatas.
- [x] Entrada atual confirmou `uwsm start`, `wayland-wm@hyprland.desktop.service` ativo
  e restauração sem duplicatas nesta entrada.
- [x] Janelas adicionais de Zen e Alacritty permaneceram no workspace de lançamento;
  configurações da Steam não herdaram a regra da janela principal.
- [ ] Janelas adicionais independentes de Telegram e Discord em aplicativos reais.
- [x] Aplicação dos cinco temas e retorno ao Studio Ember sem geração híbrida.
- [x] Preview de tema com rollback automático.
- [x] Transação de monitor expirada com restauração byte a byte da geometria.
- [x] Notificações normal/crítica, ação, histórico, DND e recuperação Dunst → SwayNC.
- [x] Fuzzel com entrada de teclado e fechamento por Escape.
- [x] Tray visível e menu de contexto implementado; barra ausente no HDMI.
- [x] Serviço oficial `swayosd-server` instalado e ativo; OSD visual exibido por
  `swayosd-client` na camada `swayosd` do DP-2.
- [x] Hyprlock renderizou nas duas escalas; opções obsoletas foram removidas.
- [x] DPMS off/on e inibidor manual de jogo.
- [x] Portais frontend, Hyprland e KDE ativos; screenshot 3840×2160 válido.
- [ ] Compartilhamento/gravação e FileChooser confirmados em aplicativos reais.
- [x] iFi e SoloCast como dispositivos padrão; SoloCast gravou PCM mono 48 kHz.
- [x] Sink iFi estava detectado porém mutado; o mute foi removido e `speaker-test`
  via PipeWire concluiu com sucesso.
- [x] Webcam capturou um quadro MJPEG 1920×1080@30 pelo V4L2.
- [x] Receptor Xbox 360 USB 045e:0719 detectado.
- [ ] Vídeo fullscreen, webcam e controle dentro de aplicativos reais; nenhum gamepad
  estava conectado ao subsistema input durante a validação do receptor.
- [x] Vulkan RADV, Gamescope e MangoHud em `vkcube`; integração GameMode inicia.
- [x] `gamemoded -t` completo passou; governador `amd_pstate`, supervisor, renice e
  prioridade de I/O foram validados.
- [x] Métricas de jogo no gap inferior do HDMI sem alterar a geometria do Chat.
- [ ] Um jogo Proton real e um jogo real via Gamescope; ficam para execução manual
  pelo usuário e não são iniciados automaticamente durante a auditoria.
- [x] HDR/10-bit somente no DP-2 e retorno a XRGB8888/sRGB.
- [ ] Logout UWSM, reboot, suspensão manual e retomada.
- [ ] Plasma Wayland reiniciado e comprovado após a instalação.

As evidências resumidas estão em `docs/validation-report.md`.
