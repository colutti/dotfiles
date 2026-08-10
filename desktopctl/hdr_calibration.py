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
        "sdrsaturation": float(tuning.get("sdrsaturation", 0.98)),
        "sdr_eotf": "srgb",
        "sdr_min_luminance": float(tuning.get("sdr_min_luminance", 0.25)),
        "sdr_max_luminance": float(tuning.get("sdr_max_luminance", 480)),
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
        self._add_scale(hdr, self.hdr_scales, "Saturação SDR", "sdrsaturation", 0.75, 1.25, 0.01, float(baseline["sdrsaturation"]), self._queue_preview)
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
        cancel = Gtk.Button(label="Cancelar")
        cancel.connect("clicked", lambda *_: self.destroy())
        actions.pack_end(cancel, False, False, 0)
        save = Gtk.Button(label="Salvar calibração")
        save.get_style_context().add_class("suggested-action")
        save.connect("clicked", self._save)
        actions.pack_end(save, False, False, 0)
        root.pack_start(actions, False, False, 0)

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
