# CachyOS workstation com DANK

Sessão Hyprland 0.56 para esta workstation CachyOS com hardware e atalhos preservados:
DANK como camada de shell, configuração modular de compositor, dois monitores e
recuperação pelo Plasma.

## Instalação

```bash
./install.sh preflight
sudo ./install.sh install
./install.sh link
./install.sh validate
```

`install` usa somente repositórios oficiais, instala `dms-shell` e mantém o
compositor/configuração do hardware sob o Hyprland desta máquina. `link` cria os
links locais necessários para a sessão e não tenta reconstruir o shell antigo.

Na tela de login, escolha a sessão Hyprland que esta máquina já usa com UWSM.

## Operação

Use o DANK para launcher, notificações, clipboard, settings, process list, lock,
brightness, audio e screenshots. As regras de monitor e os atalhos de hardware
continuam vindo do Hyprland desta máquina.

## Temas de aplicativos

As trocas de tema do DANK/Matugen também geram o CSS da interface do Zen no perfil
Flatpak e o skin do Steam em
`~/.local/share/Steam/steamui/skins/colutti-matugen/`. No primeiro uso, abra Steam em
Settings → Interface, selecione `colutti-matugen` e reinicie o Steam quando ele pedir.
As trocas seguintes apenas regeneram o skin; Steam e Zen precisam ser fechados e
abertos novamente para mostrar as novas cores.

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
