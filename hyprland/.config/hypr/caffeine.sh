#!/bin/bash

if pgrep -x hypridle >/dev/null; then
    pkill hypridle
    notify-send "󰛶  Modo always-on (sem suspensão)"
else
    hypridle &
    notify-send "󰛶  Modo normal (pode suspender)"
fi