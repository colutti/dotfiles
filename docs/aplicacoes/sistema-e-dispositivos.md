# Sistema e dispositivos

## Componentes de sessão

Além do shell principal, o desktop mantém um launcher alternativo, centro de notificações alternativo, controle visual de áudio, seletor de região para capturas, clipboard Wayland, controle de brilho, controle de mídia, wallpaper, bloqueio e redução de temperatura de cor. Eles são componentes de suporte; a reconstrução deve evitar duplicar suas funções simultaneamente na sessão.

## Integrações de dispositivo

Bluetooth, gerenciador de rede, suporte a OpenVPN, impressão, digitalização HP, exibição e controle de cor de monitores devem estar presentes. O computador usa Btrfs com snapshots e ferramentas gráficas de recuperação; o mecanismo equivalente na distribuição de destino deve oferecer restauração segura.

## Alternativas instaladas

Niri é uma alternativa de compositor disponível, mas não é a sessão principal. Fuzzel, Dunst e SwayNC estão disponíveis como alternativas de launcher e notificações; apenas uma implementação deve ser ativa em cada função. Plasma é o fallback gráfico completo.
