#!/bin/bash

# Define os workspaces para cada monitor. Esta configuração DEVE corresponder ao seu workspaces.conf.
declare -A MONITOR_WORKSPACES
MONITOR_WORKSPACES["DP-2"]="1 2 3 4 5"    # 5 workspaces para DP-2
MONITOR_WORKSPACES["HDMI-A-1"]="6 7 8 9 10" # 5 workspaces para HDMI-A-1 (do 6 ao 10)

CURRENT_WORKSPACE_ID=$(hyprctl activeworkspace -j | jq -r '.id')
CURRENT_MONITOR_NAME=$(hyprctl activeworkspace -j | jq -r '.monitor')
DIRECTION=$1 # "next" or "prev"

# Obtém a lista de workspaces SOMENTE para o monitor atual
read -ra FOCUSED_MONITOR_WORKSPACES <<< "${MONITOR_WORKSPACES[$CURRENT_MONITOR_NAME]}"

# Se o monitor atual não tiver workspaces definidos ou se houver um erro
if [ ${#FOCUSED_MONITOR_WORKSPACES[@]} -eq 0 ]; then
    echo "Erro: Nenhum workspace definido para o monitor atual ($CURRENT_MONITOR_NAME) no script."
    exit 1
fi

CURRENT_INDEX_ON_MONITOR=-1
for i in "${!FOCUSED_MONITOR_WORKSPACES[@]}"; do
   if [[ "${FOCUSED_MONITOR_WORKSPACES[$i]}" = "$CURRENT_WORKSPACE_ID" ]]; then
       CURRENT_INDEX_ON_MONITOR=$i
       break
   fi
done

# Se o workspace atual não estiver na lista de workspaces do monitor focado
if [ "$CURRENT_INDEX_ON_MONITOR" -eq -1 ]; then
    echo "Erro: Workspace atual ($CURRENT_WORKSPACE_ID) não encontrado na lista de workspaces do monitor focado ($CURRENT_MONITOR_NAME)."
    exit 1
fi

TARGET_INDEX_ON_MONITOR=-1
if [ "$DIRECTION" = "next" ]; then
    TARGET_INDEX_ON_MONITOR=$(( (CURRENT_INDEX_ON_MONITOR + 1) % ${#FOCUSED_MONITOR_WORKSPACES[@]} ))
elif [ "$DIRECTION" = "prev" ]; then
    TARGET_INDEX_ON_MONITOR=$(( (CURRENT_INDEX_ON_MONITOR - 1 + ${#FOCUSED_MONITOR_WORKSPACES[@]}) % ${#FOCUSED_MONITOR_WORKSPACES[@]} ))
else
    echo "Uso: $0 [next|prev]"
    exit 1
fi

TARGET_WORKSPACE=${FOCUSED_MONITOR_WORKSPACES[$TARGET_INDEX_ON_MONITOR]}

# Agora, apenas despachamos para o workspace alvo.
# Não há necessidade de mudar o foco do monitor, pois a navegação é local ao monitor atual.
hyprctl dispatch workspace "$TARGET_WORKSPACE"