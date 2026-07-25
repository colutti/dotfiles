#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "desktopctl" / "colutti_desktopctl.py"
THEMES = {
    "aurora-forge",
    "obsidian-glass",
    "studio-ember",
    "arctic-paper",
    "verdant-circuit",
    "nord-quiet-frost",
    "glyph-nothing",
    "aerospace-gruvbox",
}


def load_desktopctl():
    spec = importlib.util.spec_from_file_location("colutti_desktopctl", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ThemeManifestTests(unittest.TestCase):
    def test_all_versioned_themes_have_required_tokens(self):
        for slug in THEMES:
            path = ROOT / "themes" / slug / "manifest.json"
            with self.subTest(theme=slug):
                manifest = json.loads(path.read_text())
                self.assertEqual(manifest["schema_version"], 1)
                self.assertEqual(manifest["slug"], slug)
                self.assertIn(manifest["mode"], {"dark", "light"})
                self.assertGreaterEqual(manifest["contrast_ratio"], 4.5)
                self.assertEqual(
                    set(manifest["palette"]),
                    {
                        "background",
                        "surface",
                        "surface_alt",
                        "text",
                        "muted",
                        "accent",
                        "accent_alt",
                        "success",
                        "warning",
                        "critical",
                        "outline",
                    },
                )
                self.assertEqual(len(manifest["wallpaper"]["sha256"]), 64)
                self.assertTrue(manifest["wallpaper"]["source_url"].startswith("https://"))
                wallpaper = path.parent / manifest["wallpaper"]["file"]
                self.assertEqual(
                    hashlib.sha256(wallpaper.read_bytes()).hexdigest(),
                    manifest["wallpaper"]["sha256"],
                )

    def test_reference_wallpapers_are_full_source_assets_and_arctic_is_dark(self):
        expected_dimensions = {
            "glyph-nothing": "3840x2160",
            "aerospace-gruvbox": "3840x2160",
        }
        for slug, dimensions in expected_dimensions.items():
            manifest = json.loads((ROOT / "themes" / slug / "manifest.json").read_text())
            wallpaper = ROOT / "themes" / slug / manifest["wallpaper"]["file"]
            image_info = subprocess.check_output(["file", str(wallpaper)], text=True)
            self.assertIn(dimensions, image_info)
            self.assertNotIn("1920x1080", image_info)

        arctic = json.loads((ROOT / "themes" / "arctic-paper" / "manifest.json").read_text())
        self.assertEqual(arctic["mode"], "dark")
        self.assertEqual(arctic["icon_theme"], "Papirus-Dark")

    def test_theme_generation_is_deterministic_and_keeps_previous_valid_state(self):
        desktopctl = load_desktopctl()
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            first = desktopctl.ThemeManager(ROOT, state).apply("aurora-forge")
            generated = (state / "generated" / "theme.json").read_bytes()
            second = desktopctl.ThemeManager(ROOT, state).apply("aurora-forge")
            self.assertEqual(generated, (state / "generated" / "theme.json").read_bytes())
            self.assertEqual(first["slug"], second["slug"])
            self.assertIn(
                "41c7b0",
                (state / "generated" / "alacritty-theme.toml").read_text(),
            )
            self.assertIn(
                "41c7b0ff",
                (state / "generated" / "fuzzel-theme.ini").read_text(),
            )
            self.assertIn(
                "radius=14",
                (state / "generated" / "fuzzel-theme.ini").read_text(),
            )
            self.assertIn(
                "#41c7b0",
                (state / "generated" / "swaync-theme.css").read_text(),
            )
            self.assertIn(
                "window.control-center",
                (state / "generated" / "swaync-theme.css").read_text(),
            )
            self.assertIn(
                "@define-color theme_bg_color #111817",
                (state / "generated" / "gtk-theme.css").read_text(),
            )
            vscode = json.loads(
                (state / "generated" / "vscodium-theme.json").read_text()
            )
            self.assertEqual(vscode["colors"]["editor.background"], "#111817")
            kde_scheme = (state / "generated" / "ColuttiCurrent.colors").read_text()
            self.assertIn("[Colors:View]", kde_scheme)
            self.assertIn("BackgroundNormal=17,24,23", kde_scheme)
            self.assertIn("DecorationFocus=65,199,176", kde_scheme)
            self.assertIn("ColorScheme=ColuttiCurrent", kde_scheme)
            self.assertIn(
                "cosmic-cliffs.png",
                (state / "generated" / "hyprpaper.conf").read_text(),
            )
            wallpaper_config = (state / "generated" / "hyprpaper.conf").read_text()
            self.assertIn("wallpaper {", wallpaper_config)
            self.assertIn("monitor = DP-2", wallpaper_config)
            self.assertNotIn("preload =", wallpaper_config)
            self.assertNotIn("wallpaper = DP-2,", wallpaper_config)
            desktopctl.ThemeManager(ROOT, state).apply("arctic-paper")
            restored = desktopctl.ThemeManager(ROOT, state).rollback()
            self.assertEqual(restored["slug"], "aurora-forge")

    def test_theme_generation_never_publishes_a_partial_generation(self):
        desktopctl = load_desktopctl()
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            manager = desktopctl.ThemeManager(ROOT, state)
            manager.apply("aurora-forge")
            before = {
                path.name: path.read_bytes()
                for path in (state / "generated").iterdir()
            }
            original = desktopctl.atomic_text
            writes = 0

            def fail_during_generation(path, value):
                nonlocal writes
                writes += 1
                if writes == 3:
                    raise OSError("simulated generation failure")
                original(path, value)

            with mock.patch.object(desktopctl, "atomic_text", side_effect=fail_during_generation):
                with self.assertRaisesRegex(OSError, "simulated"):
                    manager.apply("arctic-paper")

            after = {
                path.name: path.read_bytes()
                for path in (state / "generated").iterdir()
            }
            self.assertEqual(before, after)
            self.assertEqual(
                json.loads((state / "generated/theme.json").read_text())["slug"],
                "aurora-forge",
            )

    def test_theme_preview_has_token_and_rolls_back_when_it_expires(self):
        desktopctl = load_desktopctl()
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            manager = desktopctl.ThemeManager(ROOT, state)
            manager.apply("aurora-forge")
            manager.apply("arctic-paper", preview=True, preview_timeout=20)
            status = json.loads((state / "theme-status.json").read_text())
            self.assertTrue(status["preview"])
            self.assertRegex(status["token"], r"^[a-f0-9]{32}$")
            self.assertEqual(status["timeout"], 20)
            self.assertTrue(manager.expire_preview(status["token"]))
            current = json.loads((state / "generated/theme.json").read_text())
            self.assertEqual(current["slug"], "aurora-forge")


class SettingsTests(unittest.TestCase):
    def test_settings_reject_unknown_keys_and_invalid_monitor_scale(self):
        desktopctl = load_desktopctl()
        valid = desktopctl.default_settings()
        desktopctl.validate_settings(valid)

        unknown = dict(valid, surprise=True)
        with self.assertRaisesRegex(ValueError, "unknown setting"):
            desktopctl.validate_settings(unknown)

        invalid = json.loads(json.dumps(valid))
        invalid["monitors"]["DP-2"]["scale"] = 0
        with self.assertRaisesRegex(ValueError, "scale"):
            desktopctl.validate_settings(invalid)

    def test_settings_validate_required_fields_and_typed_values(self):
        desktopctl = load_desktopctl()
        valid = desktopctl.default_settings()
        cases = []

        missing = json.loads(json.dumps(valid))
        del missing["profile"]
        cases.append((missing, "missing setting"))

        bad_mode = json.loads(json.dumps(valid))
        bad_mode["monitors"]["DP-2"]["mode"] = "preferred"
        cases.append((bad_mode, "mode"))

        bad_position = json.loads(json.dumps(valid))
        bad_position["monitors"]["DP-2"]["position"] = "center"
        cases.append((bad_position, "position"))

        bad_color = json.loads(json.dumps(valid))
        bad_color["monitors"]["DP-2"]["color_mode"] = "unknown"
        cases.append((bad_color, "color"))

        bad_hdr = json.loads(json.dumps(valid))
        bad_hdr["monitors"]["DP-2"]["hdr_fullscreen_passthrough"] = "yes"
        cases.append((bad_hdr, "HDR"))

        bad_theme = json.loads(json.dumps(valid))
        bad_theme["theme"] = "missing-theme"
        cases.append((bad_theme, "theme"))

        bad_dnd = json.loads(json.dumps(valid))
        bad_dnd["profile"]["dnd"] = 1
        cases.append((bad_dnd, "DND"))

        for value, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    desktopctl.validate_settings(value)

    def test_monitor_change_creates_pending_transaction_and_can_confirm(self):
        desktopctl = load_desktopctl()
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)
            manager = desktopctl.MonitorManager(ROOT, state)
            token = manager.apply(timeout=20, execute=False)
            self.assertRegex(token, r"^[a-f0-9]{32}$")
            pending = json.loads((state / "pending-monitor.json").read_text())
            self.assertEqual(pending["timeout"], 20)
            manager.confirm(token)
            self.assertFalse((state / "pending-monitor.json").exists())

    def test_monitor_apply_snapshots_live_state_and_rolls_back_partial_failure(self):
        desktopctl = load_desktopctl()
        live = [
            {
                "name": "DP-2",
                "width": 3840,
                "height": 2160,
                "refreshRate": 60.0,
                "x": 0,
                "y": 0,
                "scale": 1.67,
                "currentFormat": "XRGB8888",
                "cm": "srgb",
                "vrr": False,
            },
            {
                "name": "HDMI-A-1",
                "width": 1920,
                "height": 1080,
                "refreshRate": 60.0,
                "x": 384,
                "y": 1296,
                "scale": 1.25,
                "currentFormat": "XRGB2101010",
                "colorManagementPreset": "wide",
                "vrr": True,
            },
        ]
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state"
            config = Path(tmp) / "config"
            settings_path = config / "colutti-desktop/settings.json"
            settings_path.parent.mkdir(parents=True)
            candidate = desktopctl.default_settings()
            candidate["theme"] = "studio-ember"
            settings_path.write_text(json.dumps(candidate))
            state.mkdir(parents=True)
            previous = desktopctl.default_settings()
            previous["theme"] = "obsidian-glass"
            (state / "previous-settings.json").write_text(json.dumps(previous))
            calls: list[list[str]] = []

            def run(command, **kwargs):
                calls.append(command)
                if command[:3] == ["hyprctl", "monitors", "-j"]:
                    return subprocess.CompletedProcess(
                        command, 0, stdout=json.dumps(live), stderr=""
                    )
                apply_calls = [
                    item for item in calls
                    if item[:2] == ["hyprctl", "eval"]
                ]
                if len(apply_calls) == 2:
                    raise subprocess.CalledProcessError(1, command)
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with (
                mock.patch.dict(
                    os.environ,
                    {
                        "XDG_CONFIG_HOME": str(config),
                        "HYPRLAND_INSTANCE_SIGNATURE": "test",
                    },
                ),
                mock.patch.object(desktopctl.shutil, "which", return_value="/usr/bin/hyprctl"),
                mock.patch.object(desktopctl.subprocess, "run", side_effect=run),
            ):
                with self.assertRaises(subprocess.CalledProcessError):
                    desktopctl.MonitorManager(ROOT, state).apply()

            snapshot = json.loads((state / "last-valid-monitors.json").read_text())
            self.assertEqual(snapshot["HDMI-A-1"]["bitdepth"], 10)
            self.assertEqual(snapshot["HDMI-A-1"]["color_mode"], "wide")
            self.assertTrue(snapshot["HDMI-A-1"]["vrr"])
            self.assertFalse((state / "pending-monitor.json").exists())
            self.assertFalse((state / "previous-settings.json").exists())
            self.assertEqual(
                json.loads(settings_path.read_text())["theme"],
                "obsidian-glass",
            )
            rollback_values = [
                item[2] for item in calls
                if item[:2] == ["hyprctl", "eval"]
            ][2:]
            self.assertTrue(
                any(
                    'bitdepth = 10' in value
                    and 'cm = "wide"' in value
                    and 'vrr = 1' in value
                    for value in rollback_values
                )
            )

    def test_hdr_control_only_changes_hdr_capable_monitor(self):
        desktopctl = load_desktopctl()
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config"
            settings_path = config / "colutti-desktop/settings.json"
            settings_path.parent.mkdir(parents=True)
            settings_path.write_text(json.dumps(desktopctl.default_settings()))
            commands = []
            with (
                mock.patch.dict(
                    os.environ,
                    {
                        "XDG_CONFIG_HOME": str(config),
                        "HYPRLAND_INSTANCE_SIGNATURE": "test",
                    },
                ),
                mock.patch.object(desktopctl.shutil, "which", return_value="/usr/bin/hyprctl"),
                mock.patch.object(
                    desktopctl.subprocess,
                    "run",
                    side_effect=lambda command, **kwargs: (
                        commands.append(command)
                        or subprocess.CompletedProcess(command, 0, stdout="", stderr="")
                    ),
                ),
            ):
                result = desktopctl.MonitorManager(ROOT, Path(tmp) / "state").hdr("on")
            self.assertEqual(result["state"], "on")
            monitor_commands = [
                command for command in commands
                if command[:2] == ["hyprctl", "eval"]
            ]
            self.assertEqual(len(monitor_commands), 1)
            self.assertIn('output = "DP-2"', monitor_commands[0][2])
            self.assertIn('mode = "3840x2160@60"', monitor_commands[0][2])
            self.assertIn("scale = 1.666667", monitor_commands[0][2])
            self.assertIn("bitdepth = 10", monitor_commands[0][2])
            self.assertIn('cm = "hdr"', monitor_commands[0][2])
            self.assertIn("vrr = 0", monitor_commands[0][2])


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str, state: Path) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["COLUTTI_DESKTOP_ROOT"] = str(ROOT)
        env["COLUTTI_DESKTOP_STATE"] = str(state)
        return subprocess.run(
            [str(ROOT / "bin" / "colutti-desktopctl"), *args],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_theme_list_is_machine_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("theme", "list", "--json", state=Path(tmp))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({item["slug"] for item in json.loads(result.stdout)}, THEMES)

    def test_doctor_reports_capabilities_without_mutating_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("doctor", "--json", state=Path(tmp))
            self.assertIn(result.returncode, {0, 2}, result.stderr)
            report = json.loads(result.stdout)
            self.assertIn("checks", report)
            self.assertTrue(all("status" in check for check in report["checks"]))
            names = {check["name"] for check in report["checks"]}
            self.assertIn("portal-hyprland", names)
            self.assertIn("notification-service", names)
            self.assertIn("theme-state", names)
            self.assertIn("official-packages", names)
            self.assertIn("flatpak-apps", names)
            self.assertIn("monitor-layout", names)
            self.assertIn("primary-panel", names)
            self.assertIn("audio-defaults", names)
            self.assertIn("restored-apps", names)
            self.assertIn("storage-headroom", names)

    def test_settings_apply_validates_before_atomic_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state"
            config = root / "config"
            current = config / "colutti-desktop/settings.json"
            current.parent.mkdir(parents=True)
            current.write_text((ROOT / "settings/default.json").read_text())
            valid = json.loads(current.read_text())
            valid["theme"] = "studio-ember"
            valid_path = root / "valid.json"
            valid_path.write_text(json.dumps(valid))
            invalid = json.loads(json.dumps(valid))
            invalid["monitors"]["DP-2"]["scale"] = 0
            invalid_path = root / "invalid.json"
            invalid_path.write_text(json.dumps(invalid))

            env = os.environ.copy()
            env["COLUTTI_DESKTOP_ROOT"] = str(ROOT)
            env["COLUTTI_DESKTOP_STATE"] = str(state)
            env["XDG_CONFIG_HOME"] = str(config)
            rejected = subprocess.run(
                [
                    str(ROOT / "bin/colutti-desktopctl"),
                    "settings",
                    "apply",
                    str(invalid_path),
                ],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertEqual(json.loads(current.read_text())["theme"], "aurora-forge")
            accepted = subprocess.run(
                [
                    str(ROOT / "bin/colutti-desktopctl"),
                    "settings",
                    "apply",
                    str(valid_path),
                ],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertEqual(json.loads(current.read_text())["theme"], "studio-ember")
            rolled_back = subprocess.run(
                [
                    str(ROOT / "bin/colutti-desktopctl"),
                    "monitors",
                    "rollback",
                ],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(rolled_back.returncode, 0, rolled_back.stderr)
            self.assertEqual(json.loads(current.read_text())["theme"], "aurora-forge")


class GameProfileTests(unittest.TestCase):
    def test_game_profile_restores_exact_previous_visual_and_power_state(self):
        desktopctl = load_desktopctl()
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state"
            config = Path(tmp) / "config"
            settings = config / "colutti-desktop/settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps(desktopctl.default_settings()))
            commands: list[list[str]] = []

            def run(command, **kwargs):
                commands.append(command)
                if command == ["powerprofilesctl", "get"]:
                    return subprocess.CompletedProcess(
                        command, 0, stdout="balanced\n", stderr=""
                    )
                if command[:3] == ["hyprctl", "getoption", "animations:enabled"]:
                    return subprocess.CompletedProcess(
                        command, 0, stdout='{"bool": false}', stderr=""
                    )
                if command[:3] == ["hyprctl", "getoption", "decoration:blur:enabled"]:
                    return subprocess.CompletedProcess(
                        command, 0, stdout='{"bool": true}', stderr=""
                    )
                if command == ["swaync-client", "-D"]:
                    return subprocess.CompletedProcess(
                        command, 0, stdout="false\n", stderr=""
                    )
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with (
                mock.patch.object(desktopctl, "STATE", state),
                mock.patch.dict(
                    os.environ,
                    {
                        "XDG_CONFIG_HOME": str(config),
                        "HYPRLAND_INSTANCE_SIGNATURE": "test",
                    },
                ),
                mock.patch.object(desktopctl.shutil, "which", return_value="/usr/bin/tool"),
                mock.patch.object(desktopctl.subprocess, "run", side_effect=run),
            ):
                desktopctl.set_game_profile("on")
                desktopctl.set_game_profile("off")

            eval_commands = [
                command for command in commands if command[:2] == ["hyprctl", "eval"]
            ]
            self.assertIn("animations = { enabled = false", eval_commands[-1][2])
            self.assertIn("blur = { enabled = true", eval_commands[-1][2])
            self.assertIn(["powerprofilesctl", "set", "balanced"], commands)
            self.assertIn(
                ["systemctl", "--user", "start", "colutti-game-inhibit.service"],
                commands,
            )
            self.assertIn(
                ["systemctl", "--user", "stop", "colutti-game-inhibit.service"],
                commands,
            )
            persisted = json.loads(settings.read_text())
            self.assertEqual(persisted["profile"]["game"], "off")
            self.assertEqual(persisted["profile"]["power"], "balanced")
            self.assertFalse(persisted["profile"]["dnd"])


if __name__ == "__main__":
    unittest.main()
