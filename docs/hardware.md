# Inventário da workstation

Capturado em 24 de julho de 2026 antes da implementação.

| Componente | Identificação | Política |
|---|---|---|
| GPU | AMD Navi 31, Radeon RX 7900 XTX, `amdgpu` | Mesa/RADV; sem variáveis globais para jogos |
| Monitor principal | DP-2, BenQ EL2870U, 3840×2160@60 | escala 1.666667; HDR/10-bit com primárias EDID; SDR mapeado com brilho/saturação 1.00, preto 0.25 nit e pico 450 nits; VRR off |
| Monitor inferior | HDMI-A-1, 1920×1080@60 | escala 1.25; posição 384×1296; SDR/8-bit; DDC disponível |
| Teclado | Keychron K2 Pro, USB 3434:0221 | `es(nodeadkeys)`, Caps=Escape, 60 Hz/300 ms |
| Mouse | Logitech Unifying Receiver, USB 046d:c52b | aceleração padrão; botões laterais trocam workspace |
| Controle | Xbox 360 Wireless Adapter, USB 045e:0719 | receptor detectado; nenhum gamepad conectado durante o teste de eventos |
| Microfone | HyperX SoloCast, USB 03f0:078b | entrada padrão; captura PCM mono 48 kHz confirmada |
| Áudio | iFi HD USB Audio, USB 20b1:3008 | saída padrão confirmada no PipeWire |
| Webcam | HD WEBCAM, USB 1d6c:0103 | captura MJPEG 1920×1080@30 confirmada |

Limitações físicas conhecidas: o BenQ não anuncia VRR e seu DDC é inválido. O controle
de brilho por DDC aparece apenas no HDMI e foi validado. O HDR/10-bit pode limitar
captura e compartilhamento de tela.
