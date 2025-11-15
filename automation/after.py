"""Automation client for the After application."""
from __future__ import annotations

import time
from dataclasses import dataclass

import pyautogui

from config.loader import ApplicationSettings
from . import utils


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1


@dataclass
class AfterClient:
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

        # Pastikan fokus berada pada input username sebelum mengetik.
        for _ in range(3):
            pyautogui.hotkey("shift", "tab")
            time.sleep(0.05)

        pyautogui.hotkey("ctrl", "a")
        pyautogui.write(self.settings.username)
        pyautogui.press("tab")

        pyautogui.hotkey("ctrl", "a")
        pyautogui.write(self.settings.password)
        pyautogui.press("tab")

        pyautogui.press(self.settings.submit_key or "enter")
        time.sleep(1)

    def enter_booking(self, booking_number: str) -> None:
        utils.ensure_window_focus(self.settings.window_title)
        pyautogui.write(booking_number)
        pyautogui.press("enter")
        time.sleep(0.5)

    def dismiss_warning(self) -> None:
        """Dismiss username/password popup using Enter."""
        utils.dismiss_popup("enter")


__all__ = ["AfterClient"]
