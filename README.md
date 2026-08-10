# CachyOS/Arch workstation com DANK

Este repositório reconstrói a sessão atual da máquina `colutti`: Hyprland 0.56,
DANK/DMS, UWSM, dois monitores, regras de hardware AMD, áudio PipeWire, Steam,
Discord, Telegram, Zen, Kitty e as integrações mínimas do KDE. Ele não guarda
tokens, sessões, bibliotecas Steam, histórico de chats ou outros dados pessoais.

## Recuperação após instalação limpa

O sistema base precisa estar inicializado, com rede funcionando e com o usuário
normal `colutti` já criado. O usuário deve conseguir usar `sudo`; o bootstrap não
cria usuários, não particiona discos e não reinicia a máquina.

O DMS (`dms-shell`), Matugen e alguns componentes da sessão são distribuídos pelos
repositórios oficiais CachyOS. Se `dms-shell` não estiver disponível, o bootstrap
instala o keyring/mirrorlist oficial e habilita somente o repositório CachyOS oficial.
A política deste repositório é estritamente Arch/CachyOS oficial: não use AUR,
helpers AUR ou pacotes `*-git`.

O bootstrap instala uma política gerenciada do `pacman` que coloca helpers AUR
conhecidos em `IgnorePkg` e remove qualquer helper encontrado. Isso evita uso
acidental sem desabilitar o `makepkg` para desenvolvimento local.

Clone e execute:

```bash
sudo pacman -Syu --needed git ca-certificates
git clone https://github.com/colutti/dotfiles.git ~/projects/dotfiles
cd ~/projects/dotfiles
./install.sh bootstrap
```

O comando instala somente o que estiver faltando, usando `pacman --needed`, e faz:

- Hyprland, UWSM, DANK/DMS e a entrada `Hyprland (uwsm-managed)`;
- PipeWire, WirePlumber, portais Hyprland/GTK/KDE e polkit;
- NetworkManager, power-profiles-daemon e GameMode;
- Kitty, Fuzzel, SwayNC, Quickshell, SwayOSD, Hyprpaper, Hypridle e Hyprsunset;
- Steam, Discord, Telegram, VSCodium e Dolphin; Zen via Flatpak;
- Gamescope, MangoHud, Vulkan AMD 64/32-bit e GameMode;
- repositório multilib oficial para as dependências 32-bit da Steam e do Vulkan;
- apenas a integração KDE necessária: Dolphin, Breeze, integração GTK/Qt, ferramentas
  KDE, portal FileChooser e agente polkit. O Plasma completo não é instalado;
- links, backups, temas, Matugen, configurações do Steam e integração do Zen.

O perfil atual é detectado pelo PCI/CPU. Para a RX 7900 XTX/Navi 31, a instalação
mantém Mesa/RADV e Vulkan 64/32-bit. As regras desta máquina preservam DP-2 em
3840×2160 com escala 1.67, SDR/8-bit e VRR desligado; HDR é ativado somente
para conteúdo fullscreen compatível. HDMI-A-1 permanece em SDR/8-bit com escala 1.25.

### Simulação sem alterar o sistema

```bash
./install.sh bootstrap --dry-run
```

Esse modo detecta o perfil e resolve o plano do pacman sem instalar pacotes, criar
serviços, alterar links ou instalar Flatpaks.

### Validação descartável com Podman

```bash
./scripts/bootstrap-container-check
```

O check usa a imagem oficial `cachyos/cachyos:latest`, atualiza apenas o container
descartável, executa as verificações de sintaxe e roda o bootstrap em dry-run. O
container não comprova GPU, monitores, áudio, login UWSM ou renderização real.

## Primeiro login

Na tela de login, escolha **Hyprland (uwsm-managed)**. Depois faça login manualmente
em Steam, Discord, Telegram e Zen. A primeira seleção do skin `colutti-matugen` é
feita em Steam → Settings → Interface. A Flatpak do Zen é instalada, mas contas e
dados do perfil não são restaurados pelo repositório.

## Operação

Use o DANK para launcher, notificações, clipboard, settings, process list, lock,
brightness, áudio e screenshots. As regras de monitor e os atalhos de hardware
continuam vindo do Hyprland desta máquina.

### Steam HDR em 4K nativo

Para um jogo que ofereça HDR, selecione Proton-CachyOS SLR na compatibilidade do
jogo, habilite HDR nas opções internas dele e use em Steam → Propriedades → Geral:

```bash
DXVK_HDR=1 game-performance gamescope -f -W 3840 -H 2160 -w 3840 -h 2160 --hdr-enabled --mangoapp -- %command%
```

As resoluções interna e de saída são ambas 4K: não há upscaling. `--mangoapp` usa
o MangoHud configurado em `~/.config/MangoHud/MangoHud.conf`; não acrescente
`mangohud` ao mesmo comando. O DP-2 volta automaticamente a SDR ao encerrar o
jogo, evitando conversão SDR→HDR no desktop. O CachyOS `game-performance` é preferível ao
GameMode nesta máquina porque `ananicy-cpp` está ativo. Não use VRR, pois DP-2
não o oferece. HDR/10-bit pode limitar captura e compartilhamento de tela.

## Temas de aplicativos

As trocas de tema do DANK/Matugen geram o CSS da interface do Zen no perfil Flatpak
e o skin do Steam em
`~/.local/share/Steam/steamui/skins/colutti-matugen/`. As trocas seguintes apenas
regeneram o skin; Steam e Zen precisam ser fechados e abertos novamente para mostrar
as novas cores.

## Diagnóstico e recuperação

Depois de entrar na sessão UWSM, rode:

```bash
cd ~/projects/dotfiles
./install.sh doctor
./install.sh validate
```

Se a configuração Hyprland estiver inválida, entre no Plasma (Wayland), use
`./install.sh rollback` e consulte [`docs/recovery.md`](docs/recovery.md). O Plasma
permanece instalado e selecionável como fallback.

Arquitetura: [`docs/architecture.md`](docs/architecture.md). Atalhos:
[`docs/shortcuts.md`](docs/shortcuts.md). Evidências históricas:
[`docs/validation-report.md`](docs/validation-report.md).
