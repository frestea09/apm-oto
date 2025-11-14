"""Tkinter user interface for guiding the Frista-first workflow."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Dict

from config.loader import Settings
from workflow.session import SessionController


class MainWindow:
    """UI bertahap yang memandu operator melewati alur Frista → After."""

    def __init__(self, root: tk.Tk, controller: SessionController, settings: Settings) -> None:
        self.root = root
        self.controller = controller
        self.settings = settings

        self.status_var = tk.StringVar(value="Silakan mulai dengan login Frista.")
        self.bpjs_var = tk.StringVar()

        self._build_layout()
        self._register_callbacks()
        self._update_button_states({"frista_ready": False, "after_ready": False})

    # UI construction -------------------------------------------------
    def _build_layout(self) -> None:
        self.root.title("APM BPJS - Otomasi Frista & After")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        header = tk.Label(
            self.root,
            text="Panduan Otomasi APM",
            font=("Segoe UI", 14, "bold"),
        )
        header.pack(pady=(16, 8))

        description = tk.Label(
            self.root,
            text=(
                "Ikuti langkah di bawah ini secara berurutan. Pastikan kamera menunjukkan "
                "indikator biru sebelum mengambil foto di Frista."
            ),
            wraplength=460,
            justify="left",
        )
        description.pack(pady=(0, 12))

        # Step 1 - Frista
        frista_frame = tk.LabelFrame(self.root, text="Langkah 1 - Login Frista", padx=12, pady=12)
        frista_frame.pack(fill="x", padx=20, pady=6)

        tk.Label(
            frista_frame,
            text=(
                "Aplikasi Frista akan dibuka terlebih dahulu. Pastikan kredensial benar dan "
                "popup peringatan (jika ada) ditutup dengan tombol Spasi."
            ),
            wraplength=440,
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        self.btn_frista = tk.Button(frista_frame, text="Buka & Login Frista", width=24, command=self._on_login_frista)
        self.btn_frista.pack(side="left")

        self.btn_frista_retry = tk.Button(
            frista_frame,
            text="Coba Lagi",
            width=12,
            command=self._on_login_frista,
        )
        self.btn_frista_retry.pack(side="left", padx=(12, 0))

        # Step 2 - After
        after_frame = tk.LabelFrame(self.root, text="Langkah 2 - Login After", padx=12, pady=12)
        after_frame.pack(fill="x", padx=20, pady=6)

        tk.Label(
            after_frame,
            text=(
                "Setelah Frista siap, lanjutkan ke After. Jika muncul popup kesalahan username/password, tekan Enter."
            ),
            wraplength=440,
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        self.btn_after = tk.Button(after_frame, text="Buka & Login After", width=24, command=self._on_login_after)
        self.btn_after.pack(side="left")

        self.btn_after_retry = tk.Button(
            after_frame,
            text="Coba Lagi",
            width=12,
            command=self._on_login_after,
        )
        self.btn_after_retry.pack(side="left", padx=(12, 0))

        # Step 3 - BPJS input
        booking_frame = tk.LabelFrame(self.root, text="Langkah 3 - Input Nomor BPJS/NIK", padx=12, pady=12)
        booking_frame.pack(fill="x", padx=20, pady=6)

        tk.Label(
            booking_frame,
            text="Masukkan nomor BPJS/NIK setelah kedua aplikasi siap.",
        ).pack(anchor="w")

        entry_frame = tk.Frame(booking_frame)
        entry_frame.pack(fill="x", pady=8)

        self.entry_bpjs = tk.Entry(entry_frame, textvariable=self.bpjs_var, width=36)
        self.entry_bpjs.pack(side="left", padx=(0, 12))

        self.btn_submit = tk.Button(entry_frame, text="Kirim ke Aplikasi", command=self._on_submit_booking)
        self.btn_submit.pack(side="left")

        camera_info = tk.Label(
            booking_frame,
            text=(
                f"Kamera ID: {self.settings.camera.camera_id} | Endpoint API: {self.settings.camera.api}\n"
                "Tombol 'Ambil Foto' pada Frista akan aktif ketika kamera menunjukkan indikator biru."
            ),
            justify="left",
            wraplength=440,
        )
        camera_info.pack(anchor="w", pady=(6, 0))

        # Status & controls
        status_frame = tk.Frame(self.root, padx=20, pady=12)
        status_frame.pack(fill="x")

        status_label = tk.Label(status_frame, textvariable=self.status_var, wraplength=460, justify="left")
        status_label.pack(anchor="w")

        control_frame = tk.Frame(self.root, padx=20, pady=16)
        control_frame.pack(fill="x", pady=(0, 16))

        self.btn_reset = tk.Button(control_frame, text="Reset Alur", command=self._on_reset)
        self.btn_reset.pack(side="left")

    # Callback registration -------------------------------------------
    def _register_callbacks(self) -> None:
        self.controller.set_status_callback(self._update_status)
        self.controller.set_state_callback(self._update_button_states)
        self.controller.set_error_callback(self._show_error)
        self.controller.set_action_callback(self._handle_action_result)

    # Event handlers ---------------------------------------------------
    def _on_login_frista(self) -> None:
        self.btn_frista.config(state="disabled")
        self.btn_frista_retry.config(state="disabled")
        self.controller.login_frista_async()

    def _on_login_after(self) -> None:
        self.btn_after.config(state="disabled")
        self.btn_after_retry.config(state="disabled")
        self.controller.login_after_async()

    def _on_submit_booking(self) -> None:
        nomor = self.bpjs_var.get().strip()
        if not nomor:
            messagebox.showerror("Nomor BPJS kosong", "Masukkan nomor BPJS/NIK terlebih dahulu.")
            return
        if not nomor.isdigit():
            messagebox.showerror("Format tidak valid", "Nomor BPJS/NIK hanya boleh berisi angka.")
            return

        self.btn_submit.config(state="disabled")
        self.controller.submit_booking_async(nomor)

    def _on_reset(self) -> None:
        self.bpjs_var.set("")
        self.entry_bpjs.delete(0, tk.END)
        self.controller.reset()

    # Callback handlers ------------------------------------------------
    def _update_status(self, message: str) -> None:
        self.root.after(0, lambda: self.status_var.set(message))

    def _update_button_states(self, state: Dict[str, bool]) -> None:
        def apply_state() -> None:
            frista_ready = state.get("frista_ready", False)
            after_ready = state.get("after_ready", False)

            frista_button_state = "disabled" if frista_ready else "normal"
            self.btn_frista.config(state=frista_button_state)
            self.btn_frista_retry.config(state=frista_button_state)

            after_button_state = "normal" if frista_ready and not after_ready else "disabled"
            self.btn_after.config(state=after_button_state)
            self.btn_after_retry.config(state=after_button_state)

            if frista_ready and after_ready:
                self.entry_bpjs.config(state="normal")
                self.btn_submit.config(state="normal")
            else:
                self.entry_bpjs.config(state="disabled")
                self.btn_submit.config(state="disabled")

        self.root.after(0, apply_state)

    def _show_error(self, message: str) -> None:
        def show_message() -> None:
            messagebox.showerror("Terjadi Kesalahan", message)
        self.root.after(0, show_message)

    def _handle_action_result(self, action: str, success: bool) -> None:
        def update_controls() -> None:
            if action == "frista_login" and not success:
                self.btn_frista.config(state="normal")
                self.btn_frista_retry.config(state="normal")
            elif action == "after_login" and not success:
                if self.controller.is_frista_ready:
                    self.btn_after.config(state="normal")
                    self.btn_after_retry.config(state="normal")
            elif action == "submit_booking":
                self.btn_submit.config(state="normal")
                if success:
                    messagebox.showinfo("Berhasil", "Nomor BPJS berhasil dikirim ke Frista dan After.")
        self.root.after(0, update_controls)


__all__ = ["MainWindow"]
