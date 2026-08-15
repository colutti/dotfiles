# Sessão e desktop

## Ambientes gráficos

Hyprland é a sessão Wayland principal. Plasma permanece instalado e selecionável como fallback para recuperação e para tarefas que dependam melhor de sua integração. Não deve haver duas camadas concorrentes de barra ou de notificação na mesma sessão.

## Shell do desktop

DankMaterialShell é a camada visual principal: fornece a barra, launcher, central de controle, notificações, clipboard, tela de bloqueio, lista de processos, menus de energia e seleção de wallpaper. A barra aparece somente no monitor principal. O dock fica desativado.

A barra mostra launcher, espaços de trabalho, relógio, clima, bandeja, clipboard, notificações, bateria e acesso à central de controle. A central inclui volume, brilho, rede sem fio, saída e entrada de áudio, modo escuro e inibidor de inatividade.

## Janelas e espaços de trabalho

O layout é em mosaico. As janelas usam lacunas internas moderadas, lacunas externas maiores, cantos arredondados, borda fina e transparência discreta em janelas inativas. Animações de compositor permanecem desligadas.

Os espaços persistentes são: Web, Code, Media, Games e Focus no monitor principal; Chat, Music e Monitor no secundário. Steam e jogos abrem em Games; Discord e Telegram abrem em Chat. O navegador Zen mantém opacidade total mesmo sem foco.

## Inatividade e bloqueio

Depois de oito minutos, a temperatura de cor reduz; aos doze, a sessão bloqueia; aos quinze, os monitores desligam; aos trinta, o computador suspende. O retorno do sono deve restaurar os monitores. Inibidores legítimos de aplicações devem ser respeitados.

## Entrada

O teclado usa espanhol sem teclas mortas, com Caps Lock atuando como Escape. A repetição de teclas é rápida. O mouse principal é um Logitech MX Master, sem aceleração adicional. A experiência deve favorecer Wayland, mantendo compatibilidade com aplicações legadas quando necessária.
