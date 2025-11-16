"""Tkinter user interface for guiding the Frista-first workflow."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Optional

from automation import BarcodeScanner, BarcodeScannerError
from config.loader import Settings
from workflow.session import SessionController


class MainWindow:
    """UI bertahap yang memandu operator melewati alur Frista → After."""

    def __init__(
        self,
        root: tk.Tk,
        controller: SessionController,
        settings: Settings,
        scanner: Optional[BarcodeScanner] = None,
    ) -> None:
        self.root = root
        self.controller = controller
        self.settings = settings
        self.scanner = scanner

        self.status_var = tk.StringVar(value="Silakan mulai dengan login Frista.")
        self.bpjs_var = tk.StringVar()
        self.input_mode_var = tk.StringVar(value="manual")
        self.input_hint_var = tk.StringVar(
            value="Masukkan nomor booking secara manual jika scanner belum siap."
        )

        self._latest_state: Dict[str, bool] = {"frista_ready": False, "after_ready": False}
        self._frista_busy = False
        self._after_busy = False
        self._scanner_busy = False
        self._frista_focus_busy = False

        self._create_menubar()
        self._build_layout()
        self._register_callbacks()
        self._update_button_states({"frista_ready": False, "after_ready": False})

    # UI construction -------------------------------------------------
    def _create_menubar(self) -> None:
        menu_bar = tk.Menu(self.root)
        main_menu = tk.Menu(menu_bar, tearoff=0)
        main_menu.add_command(label="Buka Frista", command=self._on_login_frista)
        main_menu.add_command(label="Buka After", command=self._on_login_after)
        main_menu.add_separator()
        main_menu.add_command(
            label="Input Nomor Booking", command=lambda: self.entry_bpjs.focus_set() if hasattr(self, "entry_bpjs") else None
        )
        menu_bar.add_cascade(label="Menu Utama", menu=main_menu)
        menu_bar.add_command(label="Reset Alur", command=self._on_reset)
        self.root.config(menu=menu_bar)
        self.menu_bar = menu_bar

    def _build_layout(self) -> None:
        self.root.title("APM BPJS - Otomasi Frista & After")
        self.root.geometry("560x640")
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

        mode_frame = tk.Frame(booking_frame)
        mode_frame.pack(fill="x", pady=(8, 4))
        tk.Label(mode_frame, text="Sumber nomor booking:").pack(anchor="w")

        modes = [
            ("Manual", "manual"),
            ("Webcam Laptop", "webcam"),
            ("Scanner/Kamera Eksternal", "scanner"),
        ]
        radio_frame = tk.Frame(mode_frame)
        radio_frame.pack(anchor="w", pady=(4, 0))
        for label, value in modes:
            tk.Radiobutton(
                radio_frame,
                text=label,
                value=value,
                variable=self.input_mode_var,
                command=self._update_input_mode,
            ).pack(side="left", padx=(0, 12))

        entry_frame = tk.Frame(booking_frame)
        entry_frame.pack(fill="x", pady=8)

        self.entry_bpjs = tk.Entry(entry_frame, textvariable=self.bpjs_var, width=32)
        self.entry_bpjs.pack(side="left", padx=(0, 12))

        self.btn_submit = tk.Button(entry_frame, text="Kirim ke Aplikasi", command=self._on_submit_booking)
        self.btn_submit.pack(side="left", padx=(0, 8))

        self.btn_scan = tk.Button(entry_frame, text="Scan Barcode", command=self._on_scan_barcode)
        self.btn_scan.pack(side="left")

        hint_label = tk.Label(
            booking_frame,
            textvariable=self.input_hint_var,
            justify="left",
            wraplength=460,
            fg="#0f62fe",
        )
        hint_label.pack(anchor="w", pady=(0, 6))

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

        # Step 4 - Face verification reminder
        face_frame = tk.LabelFrame(
            self.root,
            text="Langkah 4 - Verifikasi Wajah & Kembali ke Menu",
            padx=12,
            pady=12,
        )
        face_frame.pack(fill="x", padx=20, pady=6)

        tk.Label(
            face_frame,
            text=(
                "Setelah pengambilan foto dan muncul popup hasil verifikasi wajah di Frista, gunakan tombol "
                "di bawah untuk menutup popup tersebut, meminimalkan Frista, dan menampilkan aplikasi utama agar "
                "operator bisa lanjut."
            ),
            wraplength=440,
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        self.btn_finish_frista = tk.Button(
            face_frame,
            text="Selesai Verifikasi di Frista",
            width=26,
            command=self._on_finish_verification,
        )
        self.btn_finish_frista.pack(anchor="w")

        # Status & controls
        status_frame = tk.Frame(self.root, padx=20, pady=12)
        status_frame.pack(fill="x")

        status_label = tk.Label(status_frame, textvariable=self.status_var, wraplength=460, justify="left")
        status_label.pack(anchor="w")

        control_frame = tk.Frame(self.root, padx=20, pady=16)
        control_frame.pack(fill="x", pady=(0, 16))

        self.btn_reset = tk.Button(control_frame, text="Reset Alur", command=self._on_reset)
        self.btn_reset.pack(side="left")

        self._set_scan_button_state()

    # Callback registration -------------------------------------------
    def _register_callbacks(self) -> None:
        self.controller.set_status_callback(self._update_status)
        self.controller.set_state_callback(self._update_button_states)
        self.controller.set_error_callback(self._show_error)
        self.controller.set_action_callback(self._handle_action_result)

    # Event handlers ---------------------------------------------------
    def _on_login_frista(self) -> None:
        self._frista_busy = True
        self.btn_frista.config(state="disabled")
        self.btn_frista_retry.config(state="disabled")
        self.controller.login_frista_async()

    def _on_login_after(self) -> None:
        self._after_busy = True
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

    def _on_scan_barcode(self) -> None:
        if not self.scanner:
            messagebox.showinfo(
                "Scanner belum dikonfigurasi",
                "Aktifkan bagian [Scanner] pada config.conf untuk menggunakan fitur ini.",
            )
            return
        if not self.scanner.is_available:
            messagebox.showerror("Scanner tidak siap", self.scanner.unavailable_reason or "Scanner tidak tersedia.")
            return
        if self._scanner_busy:
            return

        self._scanner_busy = True
        self._set_scan_button_state()
        mode = self.input_mode_var.get()
        if mode == "webcam":
            self._update_status("Mempersiapkan webcam laptop untuk membaca kartu peserta...")
        elif mode == "scanner":
            self._update_status("Mempersiapkan scanner atau kamera eksternal...")
        else:
            self._update_status("Mempersiapkan kamera barcode...")

        thread = threading.Thread(target=self._scan_barcode_task, daemon=True)
        thread.start()

    def _on_reset(self) -> None:
        self.bpjs_var.set("")
        self.entry_bpjs.delete(0, tk.END)
        self._frista_busy = False
        self._after_busy = False
        self._scanner_busy = False
        self._frista_focus_busy = False
        self.input_mode_var.set("manual")
        self._update_input_mode()
        self.controller.reset()
        self._set_scan_button_state()

    def _on_finish_verification(self) -> None:
        if self._frista_focus_busy:
            return
        if not self._latest_state.get("frista_ready", False):
            messagebox.showinfo(
                "Frista belum siap",
                "Buka dan login Frista terlebih dahulu sebelum menutupnya dari sini.",
            )
            return

        self._frista_focus_busy = True
        if hasattr(self, "btn_finish_frista"):
            self.btn_finish_frista.config(state="disabled")
        self.controller.finish_frista_async()

    # Callback handlers ------------------------------------------------
    def _update_status(self, message: str) -> None:
        self.root.after(0, lambda: self.status_var.set(message))

    def _update_button_states(self, state: Dict[str, bool]) -> None:
        self._latest_state = dict(state)

        def apply_state() -> None:
            frista_ready = self._latest_state.get("frista_ready", False)
            after_ready = self._latest_state.get("after_ready", False)

            frista_button_state = "disabled" if self._frista_busy else "normal"
            self.btn_frista.config(state=frista_button_state)
            self.btn_frista_retry.config(state=frista_button_state)

            if self._after_busy:
                after_button_state = "disabled"
            elif frista_ready:
                after_button_state = "normal"
            else:
                after_button_state = "disabled"
            self.btn_after.config(state=after_button_state)
            self.btn_after_retry.config(state=after_button_state)

            if frista_ready and after_ready:
                self.entry_bpjs.config(state="normal")
                self.btn_submit.config(state="normal")
            else:
                self.entry_bpjs.config(state="disabled")
                self.btn_submit.config(state="disabled")

            if hasattr(self, "btn_finish_frista"):
                if frista_ready and not self._frista_focus_busy:
                    self.btn_finish_frista.config(state="normal")
                else:
                    self.btn_finish_frista.config(state="disabled")

            self._set_scan_button_state()

        self.root.after(0, apply_state)

    def _show_error(self, message: str) -> None:
        def show_message() -> None:
            messagebox.showerror("Terjadi Kesalahan", message)
        self.root.after(0, show_message)

    def _handle_action_result(self, action: str, success: bool) -> None:
        def update_controls() -> None:
            if action == "frista_login":
                self._frista_busy = False
                if not success:
                    self.btn_frista.config(state="normal")
                    self.btn_frista_retry.config(state="normal")
            elif action == "after_login":
                self._after_busy = False
                if not success and self.controller.is_frista_ready:
                    self.btn_after.config(state="normal")
                    self.btn_after_retry.config(state="normal")
            elif action == "submit_booking":
                self.btn_submit.config(state="normal")
                if success:
                    messagebox.showinfo("Berhasil", "Nomor BPJS berhasil dikirim ke Frista dan After.")
            elif action == "frista_focus":
                self._frista_focus_busy = False
                if hasattr(self, "btn_finish_frista") and self._latest_state.get("frista_ready", False):
                    self.btn_finish_frista.config(state="normal")
                if success:
                    self._focus_main_window()

            if action in {"frista_login", "after_login"}:
                self._update_button_states(self._latest_state)

        self.root.after(0, update_controls)

    # Barcode helpers --------------------------------------------------
    def _scan_barcode_task(self) -> None:
        assert self.scanner is not None
        try:
            nomor = self.scanner.scan()
        except BarcodeScannerError as exc:
            self._handle_scan_failure(str(exc))
            return
        self._handle_scan_success(nomor)

    def _handle_scan_success(self, nomor: str) -> None:
        def update_entry() -> None:
            self._scanner_busy = False
            self.bpjs_var.set(nomor)
            self.entry_bpjs.config(state="normal")
            self.entry_bpjs.focus_set()
            self.entry_bpjs.selection_range(0, tk.END)
            self._update_status("Barcode terbaca. Periksa nomor sebelum dikirim.")
            self._set_scan_button_state()

        self.root.after(0, update_entry)

    def _handle_scan_failure(self, message: str) -> None:
        def show_failure() -> None:
            self._scanner_busy = False
            messagebox.showerror("Gagal memindai barcode", message)
            self._update_status("Pemindaian gagal. Coba ulangi atau isi manual.")
            self._set_scan_button_state()

        self.root.after(0, show_failure)

    def _set_scan_button_state(self) -> None:
        if not hasattr(self, "btn_scan"):
            return
        ready = self._latest_state.get("frista_ready", False) and self._latest_state.get("after_ready", False)
        mode = self.input_mode_var.get()
        label_map = {
            "manual": "Scan Barcode",
            "webcam": "Ambil dari Webcam",
            "scanner": "Scan dari Scanner",
        }
        if mode == "manual":
            state = "disabled"
        elif not ready or self._scanner_busy:
            state = "disabled"
        elif not self.scanner or not self.scanner.is_available:
            state = "disabled"
        else:
            state = "normal"
        self.btn_scan.config(state=state, text=label_map.get(mode, "Scan Barcode"))

    def _update_input_mode(self) -> None:
        hints = {
            "manual": "Masukkan nomor booking secara manual jika scanner belum siap.",
            "webcam": "Arahkan kartu BPJS ke webcam laptop lalu klik 'Ambil dari Webcam' untuk membaca barcode.",
            "scanner": "Gunakan kamera eksternal atau scanner barcode, lalu tekan tombol pemindaian saat kartu sudah siap.",
        }
        mode = self.input_mode_var.get()
        self.input_hint_var.set(hints.get(mode, hints["manual"]))
        self._set_scan_button_state()

    def _focus_main_window(self) -> None:
        def bring_to_front() -> None:
            try:
                self.root.deiconify()
            except tk.TclError:
                pass
            self.root.lift()
            self.root.focus_force()
            try:
                self.root.attributes("-topmost", True)
                self.root.after(600, lambda: self.root.attributes("-topmost", False))
            except tk.TclError:
                pass

        self.root.after(0, bring_to_front)


__all__ = ["MainWindow"]
