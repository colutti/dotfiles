# CachyOS Hyprland workstation

Sessão Hyprland 0.56 para esta workstation CachyOS: configuração Lua modular,
Quickshell próprio para a barra, Fuzzel, SwayNC, cinco temas transacionais, restauração
de aplicações, dois monitores e recuperação pelo Plasma.

## Instalação

```bash
./install.sh preflight
sudo ./install.sh install
./install.sh link
./install.sh validate
```

`install` usa somente repositórios oficiais, atualiza o sistema, cria um snapshot
Snapper quando a configuração `root` está disponível e substitui `quickshell-git` pela
versão estável. Ele não reinicia a máquina. `link` é idempotente, preserva o tema
selecionado e guarda conflitos antes de criar os links.

Na tela de login, escolha exatamente **Hyprland (uwsm-managed)**. A entrada chamada
apenas **Hyprland** funciona como compatibilidade, mas não satisfaz a arquitetura UWSM.

## Operação

```bash
colutti-desktopctl theme list
colutti-desktopctl theme preview arctic-paper
colutti-desktopctl theme apply studio-ember
colutti-desktopctl theme rollback
colutti-desktopctl monitors apply
colutti-desktopctl monitors confirm TOKEN
colutti-desktopctl monitors hdr on
colutti-desktopctl monitors hdr off
colutti-desktopctl profile game on
colutti-desktopctl profile game off
colutti-desktopctl session restore
colutti-desktopctl doctor
```

`SUPER+I` abre a GUI tipada. Mudanças de monitor têm rollback em 20 segundos; temas
também podem ser pré-visualizados com retorno automático. `colutti-game-run` combina
GameMode, MangoHud e Gamescope por jogo.

Para continuar a validação depois de reiniciar, entre na sessão UWSM, volte a este
repositório e execute:

```bash
cd ~/projects/dotfiles
./install.sh doctor
./install.sh validate
```

Arquitetura: [`docs/architecture.md`](docs/architecture.md). Atalhos:
[`docs/shortcuts.md`](docs/shortcuts.md). Recuperação:
[`docs/recovery.md`](docs/recovery.md). Evidências e pendências físicas:
[`docs/validation-report.md`](docs/validation-report.md).
