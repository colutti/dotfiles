# Repositório declarativo do desktop

## Objetivo

Transformar o repositório de dotfiles em documentação declarativa do estado
desejado do desktop pessoal. Ele deve permitir que uma pessoa ou IA entenda o
que recriar após uma formatação, em Arch, Ubuntu ou outra distribuição, sem
prescrever comandos, scripts, nomes de pacotes ou arquivos de configuração.

## Fonte de verdade

O estado observável da máquina atual é a fonte de verdade. Conteúdo já
versionado não é evidência para o inventário e será removido durante a
conversão. Divergências entre o checkout e o sistema vivo serão resolvidas em
favor do sistema vivo, salvo decisão explícita do usuário.

## Escopo

O checkout final contém somente documentos Markdown. Ele descreve hardware,
sessão gráfica, monitores, áudio, aparência, atalhos, serviços, aplicativos e
integrações, além das preferências e limitações que influenciam a reconstrução.

As informações são agrupadas por domínio para que possam ser consultadas e
mantidas isoladamente. Um índice inicial descreve o propósito, as convenções e
os limites, apontando para os documentos específicos.

## Forma de cada documento

Cada documento declara:

- estado desejado e comportamento esperado;
- relações, dependências funcionais e decisões importantes;
- aspectos que a implementação deve adaptar à distribuição ou ao hardware;
- critérios observáveis para considerar a reconstrução equivalente;
- fronteiras entre configuração e dados pessoais.

Os documentos não incluem procedimentos passo a passo, comandos, código,
scripts, manifests de pacotes, arquivos de configuração copiáveis ou detalhes
de implementação dependentes de uma distribuição.

## Estrutura inicial

```text
README.md
docs/
  estado-atual.md
  hardware.md
  sessao-e-desktop.md
  aplicacoes/
  experiencia/
  operacao/
```

A estrutura exata abaixo desses domínios pode evoluir conforme o inventário,
mas cada arquivo terá uma responsabilidade única e será ligado pelo índice.

## Dados excluídos

Credenciais, tokens, chaves, sessões autenticadas, histórico, conteúdo de
contas, bibliotecas de jogos e outros dados pessoais nunca serão registrados.
Quando relevante, a documentação informa apenas que uma autenticação ou uma
ação manual é necessária.

## Migração e verificação

Primeiro será feito um inventário somente de leitura do sistema atual. Itens
ambíguos serão confirmados com o usuário. Em seguida, serão escritos os
documentos declarativos e removido o legado técnico do checkout. A verificação
final confirma que os arquivos versionados restantes são Markdown e que o
índice alcança todos os domínios inventariados.
