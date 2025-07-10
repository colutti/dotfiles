#!/bin/bash

# --- Dynamic Workspace Configuration ---
# This script will automatically determine the workspaces for each monitor
# based on your Hyprland configuration. You only need to define them in workspaces.conf.

declare -A MONITOR_WORKSPACES

# Query Hyprland for all workspaces and their associated monitors
# This command gets a JSON array of all workspaces
HYPR_WORKSPACES_INFO=$(hyprctl workspaces -j)

# Parse the JSON to populate MONITOR_WORKSPACES.
# This jq command groups workspaces by monitor and sorts their IDs numerically.
HYPR_MONITOR_WORKSPACE_MAP=$(echo "$HYPR_WORKSPACES_INFO" | jq -r '
    group_by(.monitor) |
    map({
        "monitor": .[0].monitor,
        "workspaces": (map(.id) | sort | join(" "))
    }) |
    .[] | "\(.monitor)=\(.workspaces)"
')

# Now parse the collected string into the associative array
# The 'while read' loop is used to correctly populate the array outside of a subshell.
while IFS='=' read -r monitor_name workspace_ids; do
    MONITOR_WORKSPACES["$monitor_name"]="$workspace_ids"
done <<< "$HYPR_MONITOR_WORKSPACE_MAP"

# Optional: Add debug output to verify if MONITOR_WORKSPACES is populated correctly
# for monitor in "${!MONITOR_WORKSPACES[@]}"; do
#     echo "DEBUG: Monitor $monitor has workspaces: ${MONITOR_WORKSPACES[$monitor]}" >> /tmp/circular_workspace_debug.log
# done
# --- End Dynamic Workspace Configuration ---


CURRENT_WORKSPACE_ID=$(hyprctl activeworkspace -j | jq -r '.id')
CURRENT_MONITOR_NAME=$(hyprctl activeworkspace -j | jq -r '.monitor')
DIRECTION=$1 # "next" or "prev"

# Get the list of workspaces ONLY for the currently focused monitor
# Use printf %s\\n to split the string into separate elements for read -ra
# This ensures that if MONITOR_WORKSPACES has a value, it's correctly interpreted as an array.
if [[ -n "${MONITOR_WORKSPACES[$CURRENT_MONITOR_NAME]}" ]]; then
    read -ra FOCUSED_MONITOR_WORKSPACES <<< "${MONITOR_WORKSPACES[$CURRENT_MONITOR_NAME]}"
else
    echo "Error: No workspaces found for the current monitor ($CURRENT_MONITOR_NAME) after dynamic parsing."
    # Log the full parsed map for debugging if this error occurs
    echo "DEBUG: Parsed monitor map: $HYPR_MONITOR_WORKSPACE_MAP" >> /tmp/circular_workspace_debug.log
    exit 1
fi

# If no workspaces are defined for the current monitor or if there's an error
if [ ${#FOCUSED_MONITOR_WORKSPACES[@]} -eq 0 ]; then
    echo "Error: Empty workspace list for the current monitor ($CURRENT_MONITOR_NAME). Check your workspaces.conf."
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
    echo "Error: Current workspace ($CURRENT_WORKSPACE_ID) not found in the focused monitor's workspace list ($CURRENT_MONITOR_NAME). This can happen if a temporary workspace is active."
    # As a fallback, try to move to the next sequential workspace if the current one isn't in our defined list
    hyprctl dispatch workspace "$CURRENT_WORKSPACE_ID" # Stay on current or try to go there
    exit 1 # Exit to prevent unexpected behavior
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