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
dms doctor
systemctl --user restart dms
```

## Shell ou notificações

```bash
systemctl --user status dms
journalctl --user -u dms -b
systemctl --user restart dms
```

Se o shell entrar em `start-limit`:

```bash
systemctl --user reset-failed dms
systemctl --user restart dms
```

## Sessão iniciada pela entrada errada

`dms doctor` deve apontar o estado da sessão e das dependências. Saia com
`colutti-session-logout` e selecione a entrada Hyprland gerenciada por UWSM no
próximo login.

## Snapshot Btrfs

Liste snapshots com `sudo snapper -c root list`. A restauração do snapshot é uma operação
de sistema e deve seguir o procedimento do CachyOS/Snapper usado na máquina. Prefira
primeiro o backup de arquivos criado por `./install.sh link`.
