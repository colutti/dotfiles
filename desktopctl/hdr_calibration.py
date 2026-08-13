#!/usr/bin/env python3
"""Interactive HDR and DDC/CI calibration for the primary monitor."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, GLib, Gtk

from colutti_desktopctl import (
    STATE,
    MonitorManager,
    atomic_json,
    atomic_text,
    build_hdr_calibration_target,
    read_settings,
    render_hdr_calibration_lua,
    settings_path,
    validate_settings,
)


DDC_CODES = {
    "Brilho": "10",
    "Contraste": "12",
    "Vermelho": "16",
    "Verde": "18",
    "Azul": "1A",
}


def install_readable_style() -> None:
    provider = Gtk.CssProvider()
    provider.load_from_data(b'''
        .hdr-calibration, .hdr-calibration label, .hdr-calibration button,
        .hdr-calibration entry, .hdr-calibration combobox {
            font-family: "Noto Sans";
            font-size: 14px;
            font-stretch: normal;
        }
        .hdr-calibration button { font-weight: 600; min-height: 34px; padding: 6px 12px; }
        .hdr-calibration scale slider { min-width: 18px; min-height: 18px; }
        .hdr-calibration notebook tab { padding: 8px 12px; }
    ''')
    screen = Gdk.Screen.get_default()
    if screen is not None:
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1
        )


def initial_hdr_values(current: dict[str, object]) -> dict[str, float | str]:
    tuning = current.get("hdr_tuning", {})
    if not isinstance(tuning, dict):
        tuning = {}
    return {
        "sdrbrightness": float(tuning.get("sdrbrightness", 1.0)),
        "sdrsaturation": float(tuning.get("sdrsaturation", 1.0)),
        "sdr_eotf": "srgb",
        "sdr_min_luminance": float(tuning.get("sdr_min_luminance", 0.25)),
        "sdr_max_luminance": float(tuning.get("sdr_max_luminance", 450)),
    }


def ddc_get(code: str, bus: int) -> tuple[int, int] | None:
    result = subprocess.run(
        ["ddcutil", "getvcp", code, "--brief", "--bus", str(bus)],
        text=True,
        capture_output=True,
        check=False,
    )
    match = re.search(r"VCP\s+\S+\s+\S+\s+(\d+)\s+(\d+)", result.stdout)
    return (int(match.group(1)), int(match.group(2))) if match else None


def ddc_set(code: str, value: int, bus: int) -> bool:
    return subprocess.run(
        ["ddcutil", "setvcp", code, str(value), "--bus", str(bus)],
        text=True,
        capture_output=True,
        check=False,
    ).returncode == 0


class ReferencePatternsWindow(Gtk.Window):
    """Visual references for tuning SDR content shown through the HDR pipeline."""

    def __init__(self) -> None:
        super().__init__(title="Padrões de referência")
        self.set_default_size(1024, 760)
        self.set_border_width(18)
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        root.get_style_context().add_class("hdr-calibration")
        self.add(root)
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>Referência visual SDR em HDR</span>")
        title.set_xalign(0)
        root.pack_start(title, False, False, 0)
        hint = Gtk.Label(label=(
            "Deixe esta janela visível e ajuste os sliders na calibração. Estes padrões não medem "
            "precisão, mas expõem clipping, dominante de cor e saturação excessiva."
        ))
        hint.set_xalign(0)
        hint.set_line_wrap(True)
        root.pack_start(hint, False, False, 0)
        canvas = Gtk.DrawingArea()
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)
        canvas.connect("draw", self._draw)
        root.pack_start(canvas, True, True, 0)

    @staticmethod
    def _text(context, text: str, x: float, y: float, size: float = 14) -> None:
        context.set_source_rgb(0.84, 0.86, 0.89)
        context.select_font_face("Noto Sans", 0, 0)
        context.set_font_size(size)
        context.move_to(x, y)
        context.show_text(text)

    @staticmethod
    def _swatches(context, values: list[tuple[float, float, float]], x: float, y: float, width: float, height: float) -> None:
        step = width / len(values)
        for index, color in enumerate(values):
            context.set_source_rgb(*color)
            context.rectangle(x + index * step, y, step + 1, height)
            context.fill()

    def _draw(self, _widget: Gtk.DrawingArea, context) -> bool:
        width = _widget.get_allocated_width()
        height = _widget.get_allocated_height()
        margin = 20
        content_width = width - margin * 2
        context.set_source_rgb(0.07, 0.08, 0.10)
        context.paint()

        y = 28
        self._text(context, "Preto e detalhe em sombras", margin, y)
        y += 12
        near_black = [(level / 255,) * 3 for level in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32)]
        self._swatches(context, near_black, margin, y, content_width, 52)
        self._text(context, "0  1  2  3  4  5  6  8  10  12  16  20  24  32", margin, y + 72, 12)

        y += 112
        self._text(context, "Escala de cinza, nenhuma faixa deve parecer colorida", margin, y)
        y += 12
        gray = [(level, level, level) for level in [index / 31 for index in range(32)]]
        self._swatches(context, gray, margin, y, content_width, 62)

        y += 106
        self._text(context, "Brancos próximos, distinga os blocos sem perder detalhe", margin, y)
        y += 12
        near_white = [(level / 255,) * 3 for level in (180, 200, 216, 224, 232, 236, 240, 244, 248, 252, 255)]
        self._swatches(context, near_white, margin, y, content_width, 48)
        self._text(context, "180  200  216  224  232  236  240  244  248  252  255", margin, y + 68, 12)

        y += 108
        self._text(context, "Cores de referência, procure por vermelho fluorescente ou pele alaranjada", margin, y)
        y += 12
        reference_colors = [
            (0.95, 0.10, 0.13), (0.98, 0.35, 0.08), (0.96, 0.77, 0.08),
            (0.18, 0.70, 0.28), (0.08, 0.57, 0.85), (0.29, 0.31, 0.88),
            (0.68, 0.20, 0.72), (0.45, 0.25, 0.15), (0.76, 0.52, 0.36),
            (0.93, 0.72, 0.56), (0.99, 0.83, 0.69),
        ]
        self._swatches(context, reference_colors, margin, y, content_width, 72)

        y += 116
        self._text(context, "Rampas de saturação, pare antes de os extremos parecerem luz neon", margin, y)
        y += 12
        rows = [(0.95, 0.10, 0.13), (0.18, 0.70, 0.28), (0.08, 0.57, 0.85)]
        row_height = max(28, min(42, (height - y - 20) / 3))
        for red, green, blue in rows:
            colors = []
            for index in range(32):
                amount = index / 31
                gray_value = 0.50
                colors.append((
                    gray_value + (red - gray_value) * amount,
                    gray_value + (green - gray_value) * amount,
                    gray_value + (blue - gray_value) * amount,
                ))
            self._swatches(context, colors, margin, y, content_width, row_height)
            y += row_height + 8
        return False


class CalibrationWindow(Gtk.Window):
    def __init__(self, output: str, bus: int) -> None:
        super().__init__(title="Calibração HDR")
        self.output, self.bus = output, bus
        self.manager = MonitorManager()
        self.original = self.manager._capture_current()[output]
        self.saved = False
        self.restoring = False
        self.pending_preview = 0
        self.original_ddc: dict[str, tuple[int, int]] = {}
        self.ddc_scales: dict[str, Gtk.Scale] = {}
        self.patterns: ReferencePatternsWindow | None = None
        self.set_default_size(640, 720)
        self.set_border_width(20)
        self.connect("delete-event", self._on_delete)
        self._build()

    def _current_tuning(self) -> dict[str, float | str]:
        return initial_hdr_values(self.original)

    def _build(self) -> None:
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        root.get_style_context().add_class("hdr-calibration")
        self.add(root)
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>Calibração HDR — DP-2</span>")
        title.set_xalign(0)
        root.pack_start(title, False, False, 0)
        subtitle = Gtk.Label(label=(
            "Prévia imediata. Os controles HDR mantêm 10-bit, BT.2020 e metadados HDR ativos."
        ))
        subtitle.set_xalign(0)
        subtitle.set_line_wrap(True)
        root.pack_start(subtitle, False, False, 0)

        notebook = Gtk.Notebook()
        root.pack_start(notebook, True, True, 0)
        hdr = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=8)
        notebook.append_page(hdr, Gtk.Label(label="Hyprland / HDR"))
        baseline = self._current_tuning()
        self.hdr_scales: dict[str, Gtk.Scale] = {}
        self._add_scale(hdr, self.hdr_scales, "Brilho SDR", "sdrbrightness", 0.50, 2.00, 0.01, float(baseline["sdrbrightness"]), self._queue_preview)
        self._add_scale(hdr, self.hdr_scales, "Saturação SDR", "sdrsaturation", 0.00, 1.25, 0.01, float(baseline["sdrsaturation"]), self._queue_preview)
        self._add_scale(hdr, self.hdr_scales, "Preto SDR (nits)", "sdr_min_luminance", 0.00, 0.50, 0.01, float(baseline["sdr_min_luminance"]), self._queue_preview)
        self._add_scale(hdr, self.hdr_scales, "Pico SDR (nits)", "sdr_max_luminance", 80, 600, 5, float(baseline["sdr_max_luminance"]), self._queue_preview)
        eotf_row = Gtk.Box(spacing=12)
        eotf_row.pack_start(Gtk.Label(label="Curva SDR"), False, False, 0)
        self.eotf = Gtk.ComboBoxText()
        for identifier, label in (("srgb", "sRGB"), ("gamma22", "Gamma 2.2"), ("default", "Padrão")):
            self.eotf.append(identifier, label)
        self.eotf.set_active_id(str(baseline["sdr_eotf"]))
        self.eotf.connect("changed", self._queue_preview)
        eotf_row.pack_end(self.eotf, False, False, 0)
        hdr.pack_start(eotf_row, False, False, 0)

        physical = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=8)
        notebook.append_page(physical, Gtk.Label(label="Monitor físico (DDC/CI)"))
        notice = Gtk.Label(label=(
            "Estes valores são o OSD do BenQ e podem afetar a outra entrada do monitor (Windows)."
        ))
        notice.set_xalign(0)
        notice.set_line_wrap(True)
        physical.pack_start(notice, False, False, 0)
        self.ddc_notice = Gtk.Label(label="Os controles físicos são detectados somente quando solicitados.")
        self.ddc_notice.set_xalign(0)
        physical.pack_start(self.ddc_notice, False, False, 0)
        self.detect_ddc_button = Gtk.Button(label="Detectar controles do monitor")
        self.detect_ddc_button.connect("clicked", self._detect_ddc)
        physical.pack_start(self.detect_ddc_button, False, False, 0)

        self.status = Gtk.Label(label="Ajuste os sliders e observe a tela.")
        self.status.set_xalign(0)
        root.pack_start(self.status, False, False, 0)
        actions = Gtk.Box(spacing=10)
        restore = Gtk.Button(label="Restaurar sessão")
        restore.connect("clicked", self._restore)
        actions.pack_start(restore, False, False, 0)
        patterns = Gtk.Button(label="Abrir padrões")
        patterns.connect("clicked", self._show_patterns)
        actions.pack_start(patterns, False, False, 0)
        cancel = Gtk.Button(label="Cancelar")
        cancel.connect("clicked", lambda *_: self.destroy())
        actions.pack_end(cancel, False, False, 0)
        save = Gtk.Button(label="Salvar calibração")
        save.get_style_context().add_class("suggested-action")
        save.connect("clicked", self._save)
        actions.pack_end(save, False, False, 0)
        root.pack_start(actions, False, False, 0)

    def _show_patterns(self, *_args: object) -> None:
        if self.patterns is None:
            self.patterns = ReferencePatternsWindow()
            self.patterns.connect("destroy", lambda *_: setattr(self, "patterns", None))
        self.patterns.show_all()
        self.patterns.present()

    @staticmethod
    def _add_scale(
        container: Gtk.Box, collection: dict[str, Gtk.Scale], label: str, key: str,
        low: float, high: float, step: float, value: float, callback=None,
    ) -> None:
        row = Gtk.Box(spacing=12)
        text = Gtk.Label(label=label)
        text.set_xalign(0)
        text.set_size_request(155, -1)
        row.pack_start(text, False, False, 0)
        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, low, high, step)
        scale.set_value(value)
        scale.set_digits(0 if step >= 1 else 2)
        scale.set_hexpand(True)
        scale.set_draw_value(True)
        scale.connect("value-changed", callback or (lambda *_: None))
        row.pack_start(scale, True, True, 0)
        container.pack_start(row, False, False, 0)
        collection[key] = scale

    def _values(self) -> dict[str, float | str]:
        return {
            key: scale.get_value() for key, scale in self.hdr_scales.items()
        } | {"sdr_eotf": self.eotf.get_active_id() or "srgb"}

    def _queue_preview(self, *_args: object) -> None:
        if self.restoring:
            return
        if self.pending_preview:
            GLib.source_remove(self.pending_preview)
        self.pending_preview = GLib.timeout_add(80, self._preview)

    def _preview(self) -> bool:
        self.pending_preview = 0
        try:
            target = build_hdr_calibration_target(self.original, **self._values())
            self.manager._apply_one(self.output, target, check=True)
            self.status.set_text("Prévia aplicada em tempo real.")
        except Exception as error:
            self.status.set_text(f"Não foi possível aplicar a prévia: {error}")
        return False

    def activate_initial_preview(self) -> None:
        tuning = self.original.get("hdr_tuning", {})
        already_active = (
            self.original.get("bitdepth") == 10
            and self.original.get("color_mode") == "hdredid"
        )
        if already_active:
            self.status.set_text("HDR já está ativo. Ajuste os sliders para prévia imediata.")
            return
        self._preview()

    def _queue_ddc(self, scale: Gtk.Scale) -> None:
        if self.restoring:
            return
        for label, candidate in self.ddc_scales.items():
            if candidate is scale:
                if ddc_set(DDC_CODES[label], round(scale.get_value()), self.bus):
                    self.status.set_text(f"{label} físico aplicado.")
                else:
                    self.status.set_text(f"Não foi possível alterar {label} no monitor.")
                return

    def _detect_ddc(self, *_args: object) -> None:
        self.detect_ddc_button.set_sensitive(False)
        self.ddc_notice.set_text("Consultando o monitor…")
        while Gtk.events_pending():
            Gtk.main_iteration()
        probe = ddc_get("10", self.bus)
        if probe is None:
            self.ddc_notice.set_text(
                "DDC/CI não respondeu neste modo HDR. Use o menu físico do BenQ."
            )
            self.detect_ddc_button.set_sensitive(True)
            return
        self.original_ddc = {"Brilho": probe}
        for label, code in DDC_CODES.items():
            if label != "Brilho" and (value := ddc_get(code, self.bus)) is not None:
                self.original_ddc[label] = value
        self.ddc_notice.set_text("Controles físicos detectados.")
        for label, (current, maximum) in self.original_ddc.items():
            self._add_scale(
                self.ddc_notice.get_parent(), self.ddc_scales, label, label,
                0, maximum, 1, current, self._queue_ddc,
            )
        self.detect_ddc_button.hide()
        self.show_all()

    def _restore(self, *_args: object) -> None:
        self.restoring = True
        try:
            values = self._current_tuning()
            for key, scale in self.hdr_scales.items():
                scale.set_value(float(values[key]))
            self.eotf.set_active_id(str(values["sdr_eotf"]))
            for label, (value, _maximum) in self.original_ddc.items():
                self.ddc_scales[label].set_value(value)
        finally:
            self.restoring = False
        self.manager._apply_one(self.output, self.original, check=False)
        for label, (value, _maximum) in self.original_ddc.items():
            ddc_set(DDC_CODES[label], value, self.bus)
        self.saved = False
        self.status.set_text("Sessão restaurada ao estado de antes de abrir a janela.")

    def _save(self, *_args: object) -> None:
        target = build_hdr_calibration_target(self.original, **self._values())
        settings = read_settings()
        settings["monitors"][self.output].update({
            "bitdepth": target["bitdepth"],
            "color_mode": target["color_mode"],
            "hdr_tuning": target["hdr_tuning"],
        })
        validate_settings(settings)
        atomic_json(settings_path(), settings)
        generated = STATE / "generated/hdr-calibration.lua"
        atomic_text(generated, render_hdr_calibration_lua(self.output, target))
        self.saved = True
        self.status.set_text("Calibração salva e será reaplicada no próximo início do Hyprland.")

    def _on_delete(self, *_args: object) -> bool:
        if self.patterns is not None:
            self.patterns.destroy()
        if not self.saved:
            self._restore()
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibração HDR ao vivo")
    parser.add_argument("--output", default="DP-2")
    parser.add_argument("--bus", type=int, default=8)
    args = parser.parse_args()
    try:
        settings = Gtk.Settings.get_default()
        if settings is not None:
            settings.set_property("gtk-font-name", "Noto Sans 14")
        install_readable_style()
        window = CalibrationWindow(args.output, args.bus)
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    window.show_all()
    window.activate_initial_preview()
    Gtk.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
