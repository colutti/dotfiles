# Design System

## Visual Theme

O shell usa superfícies sólidas ou levemente translúcidas somente onde o fundo preserva
contexto. Aurora Forge é o padrão distribuído; Studio Ember é a escolha ativa nesta
máquina.
Os outros quatro temas alteram material, ritmo e paleta, mas não a arquitetura.

## Color

Tokens semânticos vêm do `manifest.json` ativo: `background`, `surface`, `surface_alt`,
`text`, `muted`, `accent`, `accent_alt`, `success`, `warning`, `critical` e `outline`.
Estados interativos usam o accent; alertas nunca dependem apenas de cor.

## Typography

Noto Sans para interface e JetBrainsMono Nerd Font para métricas, comandos e
identificadores. Escala fixa: 12 px auxiliares, 14 px corpo, 16 px títulos de painel e
22 px títulos de página. Pesos 400, 550 e 700.

## Components

Barra superior de 42 px, pills de workspace, indicadores compactos e centros laterais
progressivos. Botões compartilham raio de 10 px e estados default, hover, focus, active,
disabled e loading. Diálogos são reservados para confirmação destrutiva ou rollback de
monitor.

## Layout

Barra somente no monitor 4K; navegação e workspaces à esquerda, janela ativa ao centro,
estado e relógio à direita. O Chat no monitor inferior fica sem painel. O controle abre
no lado direito do monitor principal. Launcher é central e
orientado a teclado. A página de configurações usa navegação lateral e conteúdo em fluxo,
sem grids repetitivos de cartões.

## Motion

Transições de 150 a 220 ms com ease-out exponencial. Movimento comunica abertura,
seleção ou mudança de estado. `reducedMotion` desliga deslocamentos e mantém apenas fades
curtos.
