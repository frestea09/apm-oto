"""Utility helpers for interacting with Windows GUI applications."""
from __future__ import annotations

import os
import socket
import time
from pathlib import Path

from contextlib import closing

try:
    import pygetwindow as gw  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    gw = None  # type: ignore


class NetworkUnavailableError(ConnectionError):
    """Error raised when the required network connection is unavailable."""


def ensure_internet_connection(timeout: float = 5.0) -> None:
    """Validate that an outbound internet connection is available."""

    try:
        with closing(socket.create_connection(("8.8.8.8", 53), timeout=timeout)):
            return
    except OSError as exc:  # pragma: no cover - relies on external connectivity
        raise NetworkUnavailableError(
            "Tidak ada koneksi internet. Periksa jaringan dan coba lagi."
        ) from exc


def launch_application(executable_path: str, delay: float, working_dir: str | None = None) -> None:
    """Launch an external application and wait for a fixed delay."""

    path = os.path.expandvars(executable_path)
    if not Path(path).exists():
        raise FileNotFoundError(f"File aplikasi tidak ditemukan: {path}")

    if working_dir:
        expanded_dir = Path(os.path.expandvars(working_dir))
        cwd = expanded_dir if expanded_dir.exists() else Path(path).parent
    else:
        cwd = Path(path).parent
    try:
        import subprocess

        subprocess.Popen([path], cwd=str(cwd))
    except Exception:
        # Fallback ke startfile jika Popen gagal (misalnya pada beberapa versi Windows)
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


def minimize_window(title: str) -> bool:
    """Minimize a window by title if supported by the system."""

    if not title or gw is None:
        return False

    windows = gw.getWindowsWithTitle(title)
    for window in windows:
        try:
            if not window.isMinimized:
                window.minimize()
            return True
        except Exception:
            continue
    return False


__all__ = [
    "NetworkUnavailableError",
    "ensure_internet_connection",
    "launch_application",
    "focus_window",
    "ensure_window_focus",
    "dismiss_popup",
    "minimize_window",
]
