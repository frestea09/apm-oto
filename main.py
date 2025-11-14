"""Entry point for the APM automation desktop helper."""
from __future__ import annotations

import tkinter as tk

from automation import AfterClient, FristaClient
from config.loader import load_config
from workflow.session import SessionController
from ui.main_window import MainWindow


def main() -> None:
    settings = load_config()

    frista_client = FristaClient(settings.frista)
    after_client = AfterClient(settings.after)
    controller = SessionController(frista_client, after_client, settings.workflow)

    root = tk.Tk()
    MainWindow(root, controller, settings)
    root.mainloop()


if __name__ == "__main__":
    main()
