# Recuperação

## Voltar ao Plasma

Na tela de login, selecione **Plasma (Wayland)**. Nenhum arquivo deste repositório remove
ou substitui o Plasma, KWin ou seus portais.

## Configuração Hyprland inválida

No TTY:

```bash
Hyprland --verify-config -c ~/.config/hypr/hyprland.lua
mv ~/.config/hypr/hyprland.lua ~/.config/hypr/hyprland.lua.disabled
```

Depois entre no Plasma e rode `./install.sh rollback` a partir do repositório.

## Monitor sem imagem

Uma aplicação via CLI expira em 20 segundos e restaura a última configuração confirmada.
Para forçar o rollback pelo TTY:

```bash
colutti-desktopctl monitors rollback
systemctl --user restart colutti-desktop.target
```

## Shell ou notificações

```bash
systemctl --user status colutti-quickshell.service
journalctl --user -u colutti-quickshell.service -b
systemctl --user start colutti-notifier-fallback.service
```

Se o wallpaper entrar em `start-limit`:

```bash
systemctl --user reset-failed hyprpaper.service
systemctl --user restart hyprpaper.service
```

## Sessão iniciada pela entrada errada

`colutti-desktopctl doctor` mostra `uwsm-session: inactive` quando foi escolhida a
entrada simples. Saia com `colutti-session-logout` e selecione
**Hyprland (uwsm-managed)** no próximo login.

## Snapshot Btrfs

Liste snapshots com `sudo snapper -c root list`. A restauração do snapshot é uma operação
de sistema e deve seguir o procedimento do CachyOS/Snapper usado na máquina. Prefira
primeiro o backup de arquivos criado por `./install.sh link`.
