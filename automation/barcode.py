"""Utility class for scanning BPJS barcodes via a USB camera."""
from __future__ import annotations

import time
from typing import Optional

try:  # pragma: no cover - optional heavy dependency
    import cv2  # type: ignore
except Exception:  # pragma: no cover - runtime only
    cv2 = None  # type: ignore

try:  # pragma: no cover - optional heavy dependency
    from pyzbar import pyzbar  # type: ignore
except Exception:  # pragma: no cover - runtime only
    pyzbar = None  # type: ignore


class BarcodeScannerError(RuntimeError):
    """Base error for barcode scanner failures."""


class BarcodeScanner:
    """Simple OpenCV-based barcode reader for BPJS cards."""

    def __init__(self, camera_id: int, scan_timeout: float, window_title: str) -> None:
        self.camera_id = camera_id
        self.scan_timeout = scan_timeout
        self.window_title = window_title
        self._availability_error: Optional[str] = None
        missing: list[str] = []
        if cv2 is None:
            missing.append("opencv-python")
        if pyzbar is None:
            missing.append("pyzbar")
        if missing:
            self._availability_error = (
                "Fitur pemindaian barcode membutuhkan paket "
                + ", ".join(missing)
                + ". Jalankan 'pip install -r requirements.txt'."
            )

    # ------------------------------------------------------------------
    @property
    def is_available(self) -> bool:
        return self._availability_error is None

    @property
    def unavailable_reason(self) -> Optional[str]:
        return self._availability_error

    # ------------------------------------------------------------------
    def scan(self) -> str:
        """Scan barcode data from the configured camera."""

        if not self.is_available:
            raise BarcodeScannerError(self._availability_error or "Scanner tidak tersedia")

        cap = cv2.VideoCapture(self.camera_id)  # type: ignore[arg-type]
        if not cap.isOpened():
            raise BarcodeScannerError(
                "Kamera barcode tidak dapat dibuka. Pastikan kamera terhubung dan ID sudah benar."
            )

        deadline = time.time() + max(self.scan_timeout, 1)
        last_frame_time = time.time()
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    if time.time() - last_frame_time > 1:
                        raise BarcodeScannerError("Tidak ada frame dari kamera. Periksa koneksi kamera.")
                    continue
                last_frame_time = time.time()

                barcodes = pyzbar.decode(frame)
                if barcodes:
                    data = barcodes[0].data.decode("utf-8").strip()
                    if data:
                        cv2.destroyAllWindows()
                        return data

                cv2.imshow(self.window_title, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    raise BarcodeScannerError("Pemindaian dibatalkan oleh operator (tombol Q).")

                if time.time() > deadline:
                    raise BarcodeScannerError("Waktu pemindaian habis. Coba dekatkan barcode dan ulangi.")
        finally:
            cap.release()
            try:
                cv2.destroyAllWindows()
            except Exception:  # pragma: no cover - OpenCV cleanup
                pass


__all__ = ["BarcodeScanner", "BarcodeScannerError"]
