"""Automation client for the Frista application."""
from __future__ import annotations

import time
from dataclasses import dataclass

import pyautogui

from config.loader import ApplicationSettings
from . import utils


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1


@dataclass
class FristaClient:
    settings: ApplicationSettings

    def launch(self) -> None:
        utils.launch_application(
            self.settings.path,
            self.settings.launch_delay,
            self.settings.working_dir,
        )
        utils.ensure_window_focus(self.settings.window_title)

    def login(self) -> None:
        utils.ensure_window_focus(self.settings.window_title)
        pyautogui.write(self.settings.username)
        pyautogui.press("tab")
        pyautogui.write(self.settings.password)
        pyautogui.press("tab")
        pyautogui.press(self.settings.submit_key or "space")
        time.sleep(1)

    def enter_booking(self, booking_number: str) -> None:
        utils.ensure_window_focus(self.settings.window_title)
        pyautogui.write(booking_number)
        pyautogui.press("enter")
        time.sleep(0.5)

    def dismiss_warning(self) -> None:
        """Dismiss error popup using space as Frista's confirmation key."""
        utils.dismiss_popup("space")

    def minimize(self) -> None:
        """Minimize the Frista window so the operator can focus on APM UI."""

        if not utils.minimize_window(self.settings.window_title):
            raise RuntimeError(
                "Tidak dapat meminimalkan jendela Frista. Pastikan Frista sedang berjalan."
            )


__all__ = ["FristaClient"]
