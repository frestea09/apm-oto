"""Automation client for the Frista application."""
from __future__ import annotations

import time
from dataclasses import dataclass

import pyautogui

from config.loader import ApplicationSettings
from . import utils


FACE_RESULT_WINDOW_TITLE = "Hasil Pengenalan Wajah"


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

    def acknowledge_face_result(self) -> bool:
        """Try to close the face verification result popup if it appears."""

        handled = utils.dismiss_popup_window(FACE_RESULT_WINDOW_TITLE, key="enter")
        if handled:
            time.sleep(0.2)
        return handled

    def minimize(self) -> None:
        """Minimize the Frista window so the operator can focus on APM UI."""

        if not utils.minimize_window(self.settings.window_title):
            raise RuntimeError(
                "Tidak dapat meminimalkan jendela Frista. Pastikan Frista sedang berjalan."
            )

    def close(self) -> None:
        """Close the Frista window entirely."""

        if not utils.close_window(self.settings.window_title):
            raise RuntimeError(
                "Tidak dapat menutup jendela Frista. Pastikan aplikasinya sedang terbuka."
            )


__all__ = ["FristaClient"]
