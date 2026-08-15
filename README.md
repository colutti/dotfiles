# Desktop declarativo de Colutti

Este repositório descreve o estado desejado do desktop pessoal de Colutti. Ele não instala, configura nem automatiza o sistema: uma pessoa ou IA deve ler os documentos, detectar a distribuição e o hardware de destino e então escolher a forma apropriada de produzir os comportamentos declarados.

O estado vivo da máquina é a fonte de verdade. Esta primeira versão foi inventariada em 15 de agosto de 2026 em uma sessão CachyOS com Hyprland.

## Princípios

- Cada documento diz **o que deve existir e como deve se comportar**, nunca uma sequência de comandos, um manifesto de pacotes, código ou arquivo de configuração copiável.
- Distribuição, versão e drivers são detalhes de implementação. A reconstrução deve conservar as capacidades e restrições descritas, não imitar nomes de componentes por inércia.
- Credenciais, tokens, sessões autenticadas, chaves, históricos, bibliotecas de jogos, documentos e outros dados pessoais não fazem parte deste repositório.
- Toda alteração de máquina feita por um agente exige a atualização, no mesmo trabalho, dos documentos afetados. Alterações manuais do usuário são reconciliadas quando ele pedir `update`.

## Índice

- [Estado atual](docs/estado-atual.md)
- [Hardware](docs/hardware.md)
- [Sessão e desktop](docs/sessao-e-desktop.md)
- Aplicações: [catálogo](docs/aplicacoes/catalogo.md), [terminal e desenvolvimento](docs/aplicacoes/terminal-e-desenvolvimento.md), [navegação e produtividade](docs/aplicacoes/navegacao-e-produtividade.md), [comunicação e segurança](docs/aplicacoes/comunicacao-e-seguranca.md), [mídia e jogos](docs/aplicacoes/midia-e-jogos.md), [sistema e dispositivos](docs/aplicacoes/sistema-e-dispositivos.md)
- Experiência: [aparência](docs/experiencia/aparencia.md), [monitores](docs/experiencia/monitores.md), [atalhos](docs/experiencia/atalhos.md)
- Operação: [manutenção](docs/operacao/manutencao.md), [limites e dados pessoais](docs/operacao/limites-e-dados-pessoais.md)
