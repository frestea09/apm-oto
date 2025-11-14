"""Workflow orchestration for coordinating Frista and After automation."""
from __future__ import annotations

import threading
import time
from typing import Callable, Dict

from automation.after import AfterClient
from automation.frista import FristaClient
from config.loader import WorkflowSettings

StatusCallback = Callable[[str], None]
StateCallback = Callable[[Dict[str, bool]], None]
ErrorCallback = Callable[[str], None]
ActionCallback = Callable[[str, bool], None]


class SessionController:
    """Mengelola alur login dan input nomor BPJS untuk Frista dan After."""

    def __init__(
        self,
        frista: FristaClient,
        after: AfterClient,
        workflow: WorkflowSettings,
    ) -> None:
        self.frista = frista
        self.after = after
        self.workflow = workflow

        self.frista_ready = False
        self.after_ready = False

        self._status_callback: StatusCallback = lambda message: None
        self._state_callback: StateCallback = lambda state: None
        self._error_callback: ErrorCallback = lambda message: None
        self._action_callback: ActionCallback = lambda action, success: None

        self._lock = threading.Lock()

    # Callback setters -------------------------------------------------
    def set_status_callback(self, callback: StatusCallback) -> None:
        self._status_callback = callback

    def set_state_callback(self, callback: StateCallback) -> None:
        self._state_callback = callback

    def set_error_callback(self, callback: ErrorCallback) -> None:
        self._error_callback = callback

    def set_action_callback(self, callback: ActionCallback) -> None:
        self._action_callback = callback

    # Public API ------------------------------------------------------
    def login_frista_async(self) -> None:
        thread = threading.Thread(target=self._login_frista_task, daemon=True)
        thread.start()

    def login_after_async(self) -> None:
        thread = threading.Thread(target=self._login_after_task, daemon=True)
        thread.start()

    def submit_booking_async(self, booking_number: str) -> None:
        thread = threading.Thread(
            target=self._submit_booking_task,
            args=(booking_number,),
            daemon=True,
        )
        thread.start()

    def reset(self) -> None:
        with self._lock:
            self.frista_ready = False
            self.after_ready = False
        self._notify_state()
        self._update_status("Status direset. Silakan mulai dengan login Frista.")
        self._emit_action("reset", True)

    # Task implementations --------------------------------------------
    def _login_frista_task(self) -> None:
        self._update_status("Membuka aplikasi Frista...")
        try:
            self.frista.launch()
            self.frista.login()
        except Exception as exc:  # pragma: no cover - runtime interaction
            self._handle_error(f"Gagal login Frista: {exc}")
            self._emit_action("frista_login", False)
            return

        with self._lock:
            self.frista_ready = True
        self._notify_state()
        self._update_status("Frista siap. Lanjutkan ke login After.")
        self._emit_action("frista_login", True)

    def _login_after_task(self) -> None:
        if not self.frista_ready:
            self._handle_error("Frista belum siap. Selesaikan langkah pertama terlebih dahulu.")
            self._emit_action("after_login", False)
            return

        self._update_status("Membuka aplikasi After...")
        try:
            self.after.launch()
            self.after.login()
        except Exception as exc:  # pragma: no cover - runtime interaction
            self._handle_error(f"Gagal login After: {exc}")
            self._emit_action("after_login", False)
            return

        with self._lock:
            self.after_ready = True
        self._notify_state()
        self._update_status("After siap. Anda bisa memasukkan nomor BPJS.")
        self._emit_action("after_login", True)

    def _submit_booking_task(self, booking_number: str) -> None:
        if not self.frista_ready or not self.after_ready:
            self._handle_error("Pastikan Frista dan After sudah login sebelum memasukkan nomor BPJS.")
            self._emit_action("submit_booking", False)
            return

        self._update_status("Mengirim nomor BPJS ke Frista dan After...")
        try:
            self.frista.enter_booking(booking_number)
            time.sleep(self.workflow.post_login_delay)
            self.after.enter_booking(booking_number)
        except Exception as exc:  # pragma: no cover - runtime interaction
            self._handle_error(f"Gagal mengirim nomor BPJS: {exc}")
            self._emit_action("submit_booking", False)
            return

        self._update_status("Nomor BPJS berhasil dikirim ke kedua aplikasi.")
        self._emit_action("submit_booking", True)

    # Helpers ---------------------------------------------------------
    def _notify_state(self) -> None:
        state = {"frista_ready": self.frista_ready, "after_ready": self.after_ready}
        self._state_callback(state)

    def _update_status(self, message: str) -> None:
        self._status_callback(message)

    def _handle_error(self, message: str) -> None:
        self._error_callback(message)

    def _emit_action(self, action: str, success: bool) -> None:
        self._action_callback(action, success)

    # Read-only properties -------------------------------------------
    @property
    def is_frista_ready(self) -> bool:
        return self.frista_ready

    @property
    def is_after_ready(self) -> bool:
        return self.after_ready


__all__ = ["SessionController"]
