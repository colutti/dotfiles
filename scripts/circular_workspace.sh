#!/bin/bash

# Defines the workspaces for each monitor. This configuration MUST match your workspaces.conf.
declare -A MONITOR_WORKSPACES
MONITOR_WORKSPACES["DP-2"]="1 2 3 4 5"    # 5 workspaces for DP-2
MONITOR_WORKSPACES["HDMI-A-1"]="6 7 8 9 10" # 5 workspaces for HDMI-A-1 (from 6 to 10)

CURRENT_WORKSPACE_ID=$(hyprctl activeworkspace -j | jq -r '.id')
CURRENT_MONITOR_NAME=$(hyprctl activeworkspace -j | jq -r '.monitor')
DIRECTION=$1 # "next" or "prev"

# Get the list of workspaces ONLY for the currently focused monitor
read -ra FOCUSED_MONITOR_WORKSPACES <<< "${MONITOR_WORKSPACES[$CURRENT_MONITOR_NAME]}"

# If no workspaces are defined for the current monitor or if there's an error
if [ ${#FOCUSED_MONITOR_WORKSPACES[@]} -eq 0 ]; then
    echo "Error: No workspaces defined for the current monitor ($CURRENT_MONITOR_NAME) in the script."
    exit 1
fi

CURRENT_INDEX_ON_MONITOR=-1
for i in "${!FOCUSED_MONITOR_WORKSPACES[@]}"; do
   if [[ "${FOCUSED_MONITOR_WORKSPACES[$i]}" = "$CURRENT_WORKSPACE_ID" ]]; then
       CURRENT_INDEX_ON_MONITOR=$i
       break
   fi
done

# If the current workspace is not found in the list of focused monitor's workspaces
if [ "$CURRENT_INDEX_ON_MONITOR" -eq -1 ]; then
    echo "Error: Current workspace ($CURRENT_WORKSPACE_ID) not found in the focused monitor's workspace list ($CURRENT_MONITOR_NAME)."
    exit 1
fi

TARGET_INDEX_ON_MONITOR=-1
if [ "$DIRECTION" = "next" ]; then
    TARGET_INDEX_ON_MONITOR=$(( (CURRENT_INDEX_ON_MONITOR + 1) % ${#FOCUSED_MONITOR_WORKSPACES[@]} ))
elif [ "$DIRECTION" = "prev" ]; then
    TARGET_INDEX_ON_MONITOR=$(( (CURRENT_INDEX_ON_MONITOR - 1 + ${#FOCUSED_MONITOR_WORKSPACES[@]}) % ${#FOCUSED_MONITOR_WORKSPACES[@]} ))
else
    echo "Usage: $0 [next|prev]"
    exit 1
fi

TARGET_WORKSPACE=${FOCUSED_MONITOR_WORKSPACES[$TARGET_INDEX_ON_MONITOR]}

# Dispatch to the target workspace. No need to change monitor focus as navigation is local.
hyprctl dispatch workspace "$TARGET_WORKSPACE"