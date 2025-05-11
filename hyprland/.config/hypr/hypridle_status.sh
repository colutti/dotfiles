#!/bin/bash

if pgrep -x hypridle >/dev/null; then
    # hypridle está rodando = pode suspender
    echo -n '{"text":"󰒲","tooltip":"Modo normal (pode suspender)","class":"on"}'
else
    # hypridle foi parado = caffeine mode
    echo -n '{"text":"󰛶","tooltip":"Modo always-on (sem suspensão)","class":"off"}'
fi
