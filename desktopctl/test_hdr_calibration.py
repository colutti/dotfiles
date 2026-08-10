import unittest
from pathlib import Path

from colutti_desktopctl import build_hdr_calibration_target, render_hdr_calibration_lua


class HdrCalibrationTargetTests(unittest.TestCase):
    def test_preview_always_keeps_the_physical_hdr_contract(self):
        target = build_hdr_calibration_target(
            {
                "mode": "3840x2160@60.00",
                "position": "0x0",
                "scale": 1.666667,
                "bitdepth": 8,
                "color_mode": "srgb",
                "vrr": False,
            },
            sdrbrightness=1.0,
            sdrsaturation=0.98,
            sdr_eotf="srgb",
            sdr_min_luminance=0.25,
            sdr_max_luminance=480.0,
        )

        self.assertEqual(target["bitdepth"], 10)
        self.assertEqual(target["color_mode"], "hdredid")
        self.assertTrue(target["hdr_tuning"]["supports_hdr"])
        self.assertTrue(target["hdr_tuning"]["supports_wide_color"])
        self.assertEqual(target["hdr_tuning"]["sdr_eotf"], "srgb")
        self.assertIsInstance(target["hdr_tuning"]["sdr_max_luminance"], int)

    def test_saved_calibration_is_a_single_monitor_override(self):
        lua = render_hdr_calibration_lua(
            "DP-2",
            build_hdr_calibration_target(
                {"mode": "3840x2160@60", "position": "0x0", "scale": 1.666667},
                sdrbrightness=1.0,
                sdrsaturation=0.98,
                sdr_eotf="srgb",
                sdr_min_luminance=0.25,
                sdr_max_luminance=480,
            ),
        )

        self.assertIn('output = "DP-2"', lua)
        self.assertIn("supports_hdr = true", lua)
        self.assertIn("sdrsaturation = 0.98", lua)

    def test_every_hdr_control_is_wired_to_live_preview(self):
        source = Path(__file__).with_name("hdr_calibration.py").read_text()

        self.assertEqual(source.count("self._queue_preview)"), 5)

    def test_hdr_calibration_has_a_hyprland_shortcut(self):
        binds = Path(__file__).parents[1] / "hyprland/.config/hypr/modules/binds.lua"

        self.assertIn('hl.bind("SUPER + SHIFT + H", app("hdr-calibration")', binds.read_text())

    def test_ddc_detection_is_not_part_of_calibrator_startup(self):
        source = Path(__file__).with_name("hdr_calibration.py").read_text()
        constructor = source.split("    def __init__", 1)[1].split(
            "    def _current_tuning", 1
        )[0]

        self.assertNotIn("ddc_get(code, bus)", constructor)

    def test_calibration_launcher_focuses_an_existing_window(self):
        launcher = Path(__file__).parents[1] / "bin/hdr-calibration"

        self.assertIn("hl.dsp.focus", launcher.read_text())

    def test_ddc_detection_stops_after_the_first_unavailable_control(self):
        source = Path(__file__).with_name("hdr_calibration.py").read_text()

        self.assertIn('probe = ddc_get("10", self.bus)', source)

if __name__ == "__main__":
    unittest.main()
