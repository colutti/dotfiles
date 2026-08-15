# Manutenção da documentação

## Contrato de fonte de verdade

Estes documentos descrevem o estado desejado, não o estado histórico de um arquivo de configuração. A fonte de verdade é a máquina em uso, interpretada com as decisões explícitas do usuário quando houver ambiguidade.

## Regra para agentes

Qualquer agente que altere a máquina deve, no mesmo trabalho, atualizar todos os documentos afetados. A alteração não está concluída enquanto comportamento, atalho, aplicativo, serviço, dispositivo ou preferência modificada não estiver refletido aqui.

Se a alteração não puder ser descrita sem instruções técnicas, o agente deve registrar o resultado observável e a razão da decisão, não sua implementação.

## Alterações manuais do usuário

O usuário está dispensado da atualização imediata. Quando ele disser `update`, ou pedir atualização da documentação, o agente deve:

1. Auditar a máquina atual apenas em modo leitura.
2. Comparar aplicativos, sessão, serviços, hardware, monitores, aparência, atalhos e preferências com estes documentos.
3. Perguntar apenas sobre divergências cujo caráter desejado não seja observável.
4. Atualizar a documentação declarativa e remover fatos que já não existam.
5. Confirmar que o checkout continua contendo somente Markdown.

## Critérios de qualidade

Uma atualização é válida quando o índice continua navegável, cada afirmação de configuração descreve um resultado desejado, não há segredos ou dados pessoais, e nenhum arquivo não Markdown é rastreado. Datas de auditoria podem ser registradas quando ajudarem a indicar a atualidade de uma observação, mas não substituem a verificação do estado vivo.
