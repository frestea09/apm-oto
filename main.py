"""Entry point for the APM automation desktop helper."""
from __future__ import annotations

import tkinter as tk

from automation import AfterClient, BarcodeScanner, FristaClient
from config.loader import load_config
from workflow.session import SessionController
from ui.main_window import MainWindow


def main() -> None:
    settings = load_config()

    frista_client = FristaClient(settings.frista)
    after_client = AfterClient(settings.after)
    controller = SessionController(frista_client, after_client, settings.workflow)

    scanner = None
    if settings.scanner.enabled:
        scanner = BarcodeScanner(
            camera_id=settings.scanner.camera_id,
            scan_timeout=settings.scanner.scan_timeout,
            window_title=settings.scanner.window_title,
        )

    root = tk.Tk()
    MainWindow(root, controller, settings, scanner=scanner)
    root.mainloop()


if __name__ == "__main__":
    main()
