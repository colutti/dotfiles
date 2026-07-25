#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_installer_has_required_modes_and_no_aur_commands(self):
        installer = (ROOT / "install.sh").read_text()
        for mode in ("preflight", "install", "link", "validate", "rollback", "doctor"):
            self.assertRegex(installer, rf"\b{mode}\b")
        forbidden = re.compile(r"\b(paru|yay|trizen|pikaur)\b")
        self.assertIsNone(forbidden.search(installer))
        self.assertIn('usermod -aG gamemode -- "${desktop_user}"', installer)
        self.assertIn("timeout 5s kscreen-doctor -o", installer)

    def test_package_manifest_uses_official_repository_packages(self):
        packages = json.loads((ROOT / "packages.json").read_text())
        self.assertEqual(packages["policy"], "official-repositories-only")
        self.assertNotIn("dms-shell", packages["remove"])
        self.assertIn("quickshell", packages["install"])
        self.assertIn("uwsm", packages["install"])
        self.assertIn("fuzzel", packages["install"])
        self.assertIn("swaync", packages["install"])
        for application in ("flatpak", "steam", "telegram-desktop", "discord"):
            self.assertIn(application, packages["install"])
        for application in (
            "network-manager-applet",
            "nwg-clipman",
            "nwg-displays",
            "nwg-look",
        ):
            self.assertIn(application, packages["optional"])
        self.assertEqual(
            packages["flatpak_apps"],
            ["app.zen_browser.zen"],
        )
        self.assertEqual(len(packages["install"]), len(set(packages["install"])))

    def test_hyprland_entrypoint_loads_modular_lua(self):
        entrypoint = (ROOT / "hyprland" / ".config" / "hypr" / "hyprland.lua").read_text()
        self.assertFalse(
            (ROOT / "hyprland/.config/hypr/hyprland.conf").exists()
        )
        for module in (
            "monitors",
            "environment",
            "input",
            "workspaces",
            "rules",
            "binds",
            "appearance",
            "permissions",
            "autostart",
        ):
            self.assertIn(f'require("modules.{module}")', entrypoint)

    def test_hyprland_qt_apps_use_kde_platform_theme(self):
        uwsm_env = (ROOT / "uwsm/.config/uwsm/env").read_text()
        hypr_env = (ROOT / "hyprland/.config/hypr/modules/environment.lua").read_text()
        binds = (ROOT / "hyprland/.config/hypr/modules/binds.lua").read_text()
        self.assertIn("export QT_QPA_PLATFORMTHEME=kde", uwsm_env)
        self.assertNotIn("export QT_QPA_PLATFORM=", uwsm_env)
        self.assertNotIn("QT_AUTO_SCREEN_SCALE_FACTOR", uwsm_env)
        self.assertIn('hl.env("QT_QPA_PLATFORMTHEME", "kde")', hypr_env)
        self.assertIn('app("env QT_QPA_PLATFORMTHEME=kde dolphin")', binds)

    def test_window_close_and_animation_defaults(self):
        binds = (ROOT / "hyprland/.config/hypr/modules/binds.lua").read_text()
        appearance = (ROOT / "hyprland/.config/hypr/modules/appearance.lua").read_text()
        self.assertIn('hl.bind("ALT + Q", hl.dsp.window.close()', binds)
        self.assertNotIn('hl.bind("SUPER + Q", hl.dsp.window.close()', binds)
        self.assertIn("animations = { enabled = false", appearance)
        self.assertEqual(appearance.count('enabled = false'), 4)

    def test_gtk_defaults_match_dark_desktop_theme(self):
        for version in ("gtk-3.0", "gtk-4.0"):
            settings = (ROOT / "gtk/.config" / version / "settings.ini").read_text()
            self.assertIn("gtk-application-prefer-dark-theme=true", settings)
            self.assertIn("gtk-theme-name=Adwaita-dark", settings)

    def test_session_initialization_exports_wayland_environment_before_portals(self):
        autostart = (ROOT / "hyprland/.config/hypr/modules/autostart.lua").read_text()
        initializer = (ROOT / "scripts/session-init").read_text()
        target = (
            ROOT / "systemd/.config/systemd/user/colutti-desktop.target"
        ).read_text()
        self.assertIn("colutti-session-init", autostart)
        self.assertIn("dbus-update-activation-environment --systemd", initializer)
        self.assertIn("WAYLAND_DISPLAY", initializer)
        self.assertIn("HYPRLAND_INSTANCE_SIGNATURE", initializer)
        self.assertIn("XDG_CURRENT_DESKTOP", initializer)
        self.assertIn("plasma-foreground-booster.service", initializer)
        self.assertIn("app-discord@autostart.service", initializer)
        self.assertIn("reset-failed", initializer)
        self.assertIn("xdg-desktop-portal-hyprland.service", initializer)
        self.assertIn("xdg-desktop-portal.service", initializer)
        self.assertNotIn("colutti-session-restore.service", target)

    def test_primary_steam_window_is_persistently_routed_to_games_workspace(self):
        rules = (ROOT / "hyprland/.config/hypr/modules/rules.lua").read_text()
        self.assertIn('name = "steam-main-placement"', rules)
        self.assertIn('initial_class = "steam"', rules)
        self.assertIn('initial_title = "Steam"', rules)
        self.assertIn('workspace = "4 silent"', rules)
        self.assertIn('monitor = "DP-2"', rules)

    def test_dwindle_places_new_windows_on_the_right(self):
        appearance = (ROOT / "hyprland/.config/hypr/modules/appearance.lua").read_text()
        self.assertIn("force_split = 2", appearance)

    def test_input_profile_matches_live_keychron_and_mx_master_names(self):
        config = (ROOT / "hyprland/.config/hypr/modules/input.lua").read_text()
        self.assertIn('kb_variant = "nodeadkeys"', config)
        self.assertIn('kb_options = "caps:escape"', config)
        self.assertIn("repeat_rate = 60", config)
        self.assertIn("repeat_delay = 300", config)
        self.assertIn('name = "logitech-mx-master-1"', config)

    def test_user_units_never_use_arbitrary_sleep(self):
        for path in (ROOT / "systemd" / ".config" / "systemd" / "user").glob("*"):
            if path.is_file():
                self.assertNotRegex(path.read_text(), r"\bsleep\s+\d")

    def test_idle_dimming_uses_display_gamma_not_keyboard_leds(self):
        idle = (ROOT / "hyprland/.config/hypr/hypridle.conf").read_text()
        target = (
            ROOT / "systemd/.config/systemd/user/colutti-desktop.target"
        ).read_text()
        sunset = (
            ROOT / "systemd/.config/systemd/user/hyprsunset.service"
        ).read_text()
        self.assertNotIn("brightnessctl", idle)
        self.assertIn("hyprctl hyprsunset gamma 35", idle)
        self.assertIn("hyprctl hyprsunset reset gamma", idle)
        self.assertIn("hyprsunset.service", target)
        self.assertIn("ExecStart=/usr/bin/hyprsunset", sunset)
        inhibitor = (
            ROOT
            / "systemd/.config/systemd/user/colutti-game-inhibit.service"
        ).read_text()
        self.assertIn("systemd-inhibit", inhibitor)
        self.assertIn("--what=idle:sleep", inhibitor)

    def test_session_restore_uses_one_shot_exec_rules_and_duplicate_guard(self):
        restore = (ROOT / "scripts" / "session-restore").read_text()
        self.assertNotIn("set -e", restore)
        self.assertIn("restore_app()", restore)
        self.assertIn("restore failed for", restore)
        self.assertIn("reconcile_chat_pair()", restore)
        self.assertIn("x = 423, y = 820", restore)
        self.assertIn("window_address", restore)
        self.assertIn("pgrep -f", restore)
        self.assertIn("reconcile_window", restore)
        self.assertIn('if [[ -n "${address}" ]]; then', restore)
        self.assertIn('reconcile_window "${address}" "${mode}"', restore)
        self.assertIn("hl.dsp.exec_cmd", restore)
        self.assertIn('size = \\"${width} ${height}\\"', restore)
        self.assertIn('move = \\"${x} ${y}\\"', restore)
        self.assertIn("hl.dsp.window.resize", restore)
        self.assertIn('workspace = \\"', restore)
        self.assertNotIn("hyprctl dispatch workspace", restore)
        self.assertNotIn("hyprctl dispatch focusmonitor", restore)
        self.assertNotIn("XDG_ACTIVATION_TOKEN", restore)
        self.assertIn("flatpak run app.zen_browser.zen", restore)
        self.assertIn("start_once app.zen_browser.zen tiled", restore)
        self.assertIn("start_once Alacritty tiled", restore)
        self.assertIn("start_once steam tiled", restore)
        self.assertIn("start_once org.telegram.desktop tiled 6 HDMI-A-1", restore)
        self.assertIn("start_once discord tiled 6 HDMI-A-1", restore)

    def test_portal_override_uses_high_priority_generic_filename(self):
        portal = ROOT / "xdg-desktop-portal/.config/xdg-desktop-portal/portals.conf"
        content = portal.read_text()
        self.assertIn("default=hyprland;kde;", content)
        self.assertIn("org.freedesktop.impl.portal.FileChooser=kde;", content)

    def test_shell_overlays_are_layer_shell_windows_not_floating_windows(self):
        shell = (ROOT / "quickshell/.config/quickshell/colutti/shell.qml").read_text()
        self.assertNotIn("FloatingWindow {", shell)
        self.assertEqual(shell.count("PanelWindow {"), 2)
        self.assertNotIn("NotificationServer", shell)
        self.assertNotIn("launcherWindow", shell)
        self.assertNotIn("controlCenter", shell)
        self.assertIn('root.run("fuzzel")', shell)
        self.assertIn('root.run("swaync-client -t -sw")', shell)
        self.assertIn('screen.name === "DP-2"', shell)
        self.assertEqual(shell.count('screen.name === "HDMI-A-1"'), 1)
        self.assertIn("visible: root.gameMode", shell)
        self.assertIn("exclusiveZone: 0", shell)
        self.assertIn("parsed.panel", shell)
        self.assertIn("Hyprland.activeToplevel.title", shell)
        self.assertIn("modelData.display(bar", shell)
        self.assertIn("Qt.RightButton", shell)
        self.assertNotIn("NumberAnimation", shell)

    def test_mature_launcher_and_notification_center_are_configured(self):
        fuzzel = (ROOT / "fuzzel/.config/fuzzel/fuzzel.ini").read_text()
        swaync = json.loads((ROOT / "swaync/.config/swaync/config.json").read_text())
        wrapper = (ROOT / "bin/colutti-desktopctl").read_text()
        desktopctl = (ROOT / "desktopctl/colutti_desktopctl.py").read_text()
        self.assertIn("exit-on-keyboard-focus-loss=yes", fuzzel)
        self.assertIn("Noto Sans:size=14", fuzzel)
        self.assertIn(
            "include=~/.local/state/colutti-desktop/generated/fuzzel-theme.ini",
            fuzzel,
        )
        swaync_css = (ROOT / "swaync/.config/swaync/style.css").read_text()
        self.assertIn("generated/swaync-theme.css", swaync_css)
        self.assertNotIn("@define-color background", swaync_css)
        self.assertIn("volume", swaync["widgets"])
        self.assertIn("mpris", swaync["widgets"])
        self.assertIn("dnd", swaync["widgets"])
        self.assertIn('readlink -f -- "${BASH_SOURCE[0]}"', wrapper)
        self.assertIn('["swaync-client", "-D"]', desktopctl)
        self.assertNotIn('"qs", "ipc", "call", "control"', desktopctl)

    def test_theme_outputs_cover_gtk_and_vscodium(self):
        package = json.loads(
            (
                ROOT
                / "vscodium/.vscode-oss/extensions/colutti-desktop-theme/package.json"
            ).read_text()
        )
        self.assertEqual(package["contributes"]["themes"][0]["label"], "Colutti Current")
        desktopctl = (
            ROOT / "desktopctl/colutti_desktopctl.py"
        ).read_text()
        self.assertIn("destination.symlink_to(source)", desktopctl)
        self.assertIn('inactive_border = "rgba({palette["outline"].lstrip("#")}ff)"', desktopctl)
        self.assertNotIn('inactive_border = "rgba({palette["outline"].lstrip("#")}aa)"', desktopctl)
        for version in ("gtk-3.0", "gtk-4.0"):
            css = (ROOT / "gtk/.config" / version / "gtk.css").read_text()
            self.assertIn("generated/gtk-theme.css", css)
        installer = (ROOT / "install.sh").read_text()
        self.assertIn("vscodium", installer)
        self.assertIn("gtk", installer)
        lock = (ROOT / "hyprland/.config/hypr/hyprlock.conf").read_text()
        self.assertIn("check_color = $success", lock)
        self.assertIn("fail_color = $critical", lock)
        for obsolete in (
            "no_fade_in",
            "no_fade_out",
            "disable_loading_bar",
            "dots_color",
            "fail_transition",
        ):
            self.assertNotIn(obsolete, lock)
        permissions = (
            ROOT / "hyprland/.config/hypr/modules/permissions.lua"
        ).read_text()
        self.assertIn('hyprlock", "screencopy", "allow"', permissions)

    def test_theme_reload_updates_hyprpaper_over_ipc_without_restart_storm(self):
        desktopctl = (
            ROOT / "desktopctl/colutti_desktopctl.py"
        ).read_text()
        self.assertIn('"hyprpaper", "listactive"', desktopctl)
        self.assertIn('"hyprpaper",', desktopctl)
        self.assertIn('"wallpaper",', desktopctl)
        self.assertIn('"reset-failed", "hyprpaper.service"', desktopctl)
        self.assertNotIn(
            '["systemctl", "--user", "try-restart", "hyprpaper.service"]',
            desktopctl,
        )

    def test_doctor_checks_live_desktop_services(self):
        desktopctl = (
            ROOT / "desktopctl/colutti_desktopctl.py"
        ).read_text()
        for unit in (
            "wayland-wm@hyprland.desktop.service",
            "colutti-quickshell.service",
            "hyprpaper.service",
            "hypridle.service",
            "hyprsunset.service",
            "colutti-clipboard.service",
            "swaync.service",
        ):
            self.assertIn(f'"{unit}"', desktopctl)

    def test_plasma_only_autostarts_do_not_pollute_hyprland(self):
        for name in (
            "discord.desktop",
            "steam.desktop",
            "org.telegram.desktop.desktop",
            "arch-update-tray.desktop",
        ):
            content = (ROOT / "autostart/.config/autostart" / name).read_text()
            self.assertTrue(
                "OnlyShowIn=KDE;" in content or "NotShowIn=Hyprland;" in content,
                name,
            )

    def test_chat_clients_are_persistently_routed_to_lower_monitor(self):
        rules = (ROOT / "hyprland/.config/hypr/modules/rules.lua").read_text()
        self.assertIn('name = "chat-discord-placement"', rules)
        self.assertIn('initial_class = "discord"', rules)
        self.assertIn('name = "chat-telegram-placement"', rules)
        self.assertIn('initial_class = "org.telegram.desktop"', rules)
        self.assertIn('workspace = "6 silent"', rules)
        self.assertIn('monitor = "HDMI-A-1"', rules)
        self.assertIn('name = "zen-no-compositor-border"', rules)
        self.assertIn('initial_class = "app.zen_browser.zen"', rules)
        self.assertIn("border_size = 0", rules)

    def test_stale_localsend_autostart_is_disabled(self):
        content = (
            ROOT / "autostart/.config/autostart/localsend_app.desktop"
        ).read_text()
        self.assertIn("Hidden=true", content)
        self.assertNotIn("Exec=", content)

    def test_notification_fallback_retries_primary_daemon(self):
        fallback = (
            ROOT
            / "systemd/.config/systemd/user/colutti-notifier-fallback.service"
        ).read_text()
        dropin = (
            ROOT
            / "systemd/.config/systemd/user/swaync.service.d/colutti.conf"
        ).read_text()
        timer = (
            ROOT
            / "systemd/.config/systemd/user/colutti-notifier-recovery.timer"
        ).read_text()
        self.assertIn("OnFailure=colutti-notifier-fallback.service", dropin)
        self.assertIn("Wants=colutti-notifier-recovery.timer", fallback)
        self.assertIn("--no-block start swaync.service", fallback)
        self.assertIn("Conflicts=swaync.service", fallback)
        self.assertIn("OnActiveSec=30s", timer)
        self.assertIn("Unit=swaync.service", timer)

    def test_audio_keys_use_mature_osd_with_runtime_fallback(self):
        binds = (ROOT / "hyprland/.config/hypr/modules/binds.lua").read_text()
        wrapper = (ROOT / "scripts/audio-control").read_text()
        unit = (
            ROOT / "systemd/.config/systemd/user/swayosd-server.service"
        ).read_text()
        self.assertIn("colutti-audio-control raise", binds)
        self.assertIn("colutti-audio-control mic-mute", binds)
        self.assertIn('SUPER + I", app("colutti-settings-gui")', binds)
        self.assertIn("swayosd-client", wrapper)
        self.assertIn("wpctl", wrapper)
        self.assertIn("ConditionPathExists=/usr/bin/swayosd-server", unit)

    def test_control_center_reuses_mature_configuration_tools(self):
        swaync = json.loads(
            (ROOT / "swaync/.config/swaync/config.json").read_text()
        )
        actions = swaync["widget-config"]["buttons-grid#actions"]["actions"]
        commands = {action["command"] for action in actions}
        for component in ("audio", "network", "displays", "appearance", "clipboard"):
            self.assertIn(f"colutti-settings-open {component}", commands)
        wrapper = (ROOT / "scripts/settings-open").read_text()
        self.assertIn("pavucontrol", wrapper)
        self.assertIn("nm-connection-editor", wrapper)
        self.assertIn("nwg-displays", wrapper)
        self.assertIn("nwg-look", wrapper)
        self.assertIn("nwg-clipman", wrapper)
        logout = (ROOT / "scripts/session-logout").read_text()
        self.assertIn("wayland-wm@hyprland.desktop.service", logout)
        self.assertIn("exec uwsm stop", logout)
        self.assertIn("hyprctl dispatch exit", logout)

    def test_primary_bar_reports_connectivity_audio_privacy_and_power(self):
        status = (ROOT / "scripts/status-line").read_text()
        shell = (
            ROOT / "quickshell/.config/quickshell/colutti/shell.qml"
        ).read_text()
        for command in ("nmcli", "tailscale", "wpctl", "pw-dump", "powerprofilesctl"):
            self.assertIn(command, status)
        for token in ("NET", "TS", "VOL", "MIC", "CAM", "SHARE", "PWR"):
            self.assertIn(token, status)
        self.assertIn("statusProcess", shell)
        self.assertIn("root.statusText", shell)
        metrics = (ROOT / "scripts/metrics-line").read_text()
        for token in ("gpu_busy_percent", "k10temp", "amdgpu", "RAM", "SSD"):
            self.assertIn(token, metrics)
        self.assertIn('screen.name === "HDMI-A-1"', shell)
        self.assertIn("visible: root.gameMode", shell)
        self.assertIn("implicitHeight: 20", shell)

    def test_game_launcher_composes_gamemode_mangohud_and_gamescope(self):
        launcher = (ROOT / "scripts/game-run").read_text()
        self.assertIn("gamemoderun", launcher)
        self.assertIn("MANGOHUD=1", launcher)
        self.assertIn("gamescope", launcher)
        self.assertIn("--mangoapp", launcher)
        self.assertIn("--gamescope", launcher)
        self.assertIn("--mangohud", launcher)
        rules = (ROOT / "hyprland/.config/hypr/modules/rules.lua").read_text()
        self.assertIn('name = "gamescope-placement"', rules)
        self.assertIn('initial_class = "gamescope"', rules)
        self.assertIn('workspace = "4 silent"', rules)

    def test_ddc_brightness_targets_only_valid_hdmi_monitor(self):
        control = (ROOT / "scripts/brightness-control").read_text()
        self.assertIn("HDMI-A-1", control)
        self.assertIn("ddcutil detect --brief", control)
        self.assertIn("setvcp 10", control)
        self.assertNotIn("DP-2", control)

    def test_settings_gui_uses_typed_cli_and_monitor_confirmation(self):
        gui = (ROOT / "scripts/settings-gui").read_text()
        self.assertIn("PySide6", gui)
        self.assertIn('["settings", "apply"', gui)
        self.assertIn('["monitors", "apply"', gui)
        self.assertIn('["monitors", "confirm"', gui)
        self.assertIn('["monitors", "rollback"]', gui)
        self.assertIn("20", gui)
        self.assertNotIn("modules/", gui)
        rules = (ROOT / "hyprland/.config/hypr/modules/rules.lua").read_text()
        self.assertIn('initial_title = "Colutti Desktop"', rules)
        self.assertIn('name = "settings-dialog"', rules)

    def test_link_backs_up_conflicts_and_rollback_restores_original_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            state = Path(tmp) / "state"
            hypr = home / ".config/hypr/hyprland.lua"
            alacritty = home / ".config/alacritty/alacritty.toml"
            hypr.parent.mkdir(parents=True)
            alacritty.parent.mkdir(parents=True)
            hypr.write_text("original hypr\n")
            alacritty.write_text("original alacritty\n")
            settings = home / ".config/colutti-desktop/settings.json"
            settings.parent.mkdir(parents=True)
            desired = json.loads((ROOT / "settings/default.json").read_text())
            desired["theme"] = "studio-ember"
            settings.write_text(json.dumps(desired))
            codium = home / ".config/VSCodium/User/settings.json"
            codium.parent.mkdir(parents=True)
            codium.write_text('{"editor.fontSize": 14}\n')
            env = os.environ.copy()
            env.update({"HOME": str(home), "XDG_STATE_HOME": str(state)})

            linked = subprocess.run(
                [str(ROOT / "install.sh"), "link"],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(linked.returncode, 0, linked.stderr)
            self.assertTrue(hypr.is_symlink())
            self.assertTrue(alacritty.is_symlink())
            swaync_dropin = (
                home
                / ".config/systemd/user/swaync.service.d/colutti.conf"
            )
            self.assertTrue(swaync_dropin.is_symlink())
            self.assertFalse(swaync_dropin.parent.is_symlink())
            active_theme = json.loads(
                (
                    state / "colutti-desktop/generated/theme.json"
                ).read_text()
            )
            self.assertEqual(active_theme["slug"], "studio-ember")

            relinked = subprocess.run(
                [str(ROOT / "install.sh"), "link"],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(relinked.returncode, 0, relinked.stderr)
            backup_homes = list(
                (state / "colutti-desktop/backups").glob("*/home")
            )
            self.assertEqual(len(backup_homes), 1)
            self.assertFalse(
                (
                    backup_homes[0]
                    / ".config/VSCodium/User/User"
                ).exists()
            )

            restored = subprocess.run(
                [str(ROOT / "install.sh"), "rollback"],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            self.assertEqual(restored.returncode, 0, restored.stderr)
            self.assertFalse(hypr.is_symlink())
            self.assertFalse(alacritty.is_symlink())
            self.assertEqual(hypr.read_text(), "original hypr\n")
            self.assertEqual(alacritty.read_text(), "original alacritty\n")


if __name__ == "__main__":
    unittest.main()
