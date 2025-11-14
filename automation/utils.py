"""Utility helpers for interacting with Windows GUI applications."""
from __future__ import annotations

import os
import time
from pathlib import Path

try:
    import pygetwindow as gw  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    gw = None  # type: ignore


def launch_application(executable_path: str, delay: float) -> None:
    """Launch an external application and wait for a fixed delay."""
    path = os.path.expandvars(executable_path)
    if not Path(path).exists():
        raise FileNotFoundError(f"File aplikasi tidak ditemukan: {path}")

    os.startfile(path)
    if delay > 0:
        time.sleep(delay)


def focus_window(title: str) -> bool:
    """Attempt to focus a window by its title."""
    if not title:
        return False
    if gw is None:
        return False

    windows = gw.getWindowsWithTitle(title)
    for window in windows:
        try:
            if window.isMinimized:
                window.restore()
            window.activate()
            return True
        except Exception:
            continue
    return False


def ensure_window_focus(title: str, timeout: float = 5.0, poll_interval: float = 0.5) -> bool:
    """Repeatedly try to focus a window until timeout."""
    end = time.time() + timeout
    while time.time() < end:
        if focus_window(title):
            return True
        time.sleep(poll_interval)
    return False


def dismiss_popup(key: str, delay: float = 0.2) -> None:
    """Dismiss a popup dialog by sending a key press."""
    try:
        import pyautogui
    except ImportError as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError("pyautogui diperlukan untuk fungsi dismiss_popup") from exc

    pyautogui.press(key)
    if delay > 0:
        time.sleep(delay)


__all__ = ["launch_application", "focus_window", "ensure_window_focus", "dismiss_popup"]
