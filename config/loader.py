"""Configuration loader for the APM automation toolkit."""
from __future__ import annotations

import os
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


DEFAULT_CONFIG_PATH = Path("config.conf")


def _get_env_key(section: str, option: str) -> str:
    return f"{section}_{option}".upper().replace(" ", "_")


def _read_optional(
    parser: ConfigParser,
    section: str,
    option: str,
    env_key: Optional[str] = None,
) -> Optional[str]:
    """Mengambil nilai dari environment atau berkas konfigurasi jika tersedia."""

    key = env_key or _get_env_key(section, option)
    env_value = os.getenv(key)
    if env_value is not None:
        return env_value
    if parser.has_section(section) and parser.has_option(section, option):
        return parser.get(section, option)
    return None


def _read_value(
    parser: ConfigParser,
    section: str,
    option: str,
    fallback: Optional[str] = None,
    env_key: Optional[str] = None,
) -> str:
    value = _read_optional(parser, section, option, env_key=env_key)
    if value is not None:
        return value
    if fallback is None:
        raise KeyError(f"Konfigurasi '{section}.{option}' tidak ditemukan dan tidak memiliki default")
    return fallback


def _read_int(
    parser: ConfigParser,
    section: str,
    option: str,
    fallback: Optional[int] = None,
    env_key: Optional[str] = None,
) -> int:
    value = _read_optional(parser, section, option, env_key=env_key)
    if value is None:
        if fallback is None:
            raise KeyError(f"Konfigurasi integer '{section}.{option}' tidak ditemukan dan tidak memiliki default")
        return fallback
    return int(value)


def _read_float(
    parser: ConfigParser,
    section: str,
    option: str,
    fallback: Optional[float] = None,
    env_key: Optional[str] = None,
) -> float:
    value = _read_optional(parser, section, option, env_key=env_key)
    if value is None:
        if fallback is None:
            raise KeyError(f"Konfigurasi float '{section}.{option}' tidak ditemukan dan tidak memiliki default")
        return fallback
    return float(value)


@dataclass
class ApplicationSettings:
    """Konfigurasi untuk aplikasi eksternal seperti Frista atau After."""

    path: str
    username: str
    password: str
    window_title: str
    launch_delay: float
    submit_key: str
    working_dir: str | None = None


@dataclass
class CameraSettings:
    camera_id: int
    api: str


@dataclass
class WorkflowSettings:
    post_login_delay: float
    network_timeout: float


@dataclass
class Settings:
    frista: ApplicationSettings
    after: ApplicationSettings
    camera: CameraSettings
    workflow: WorkflowSettings


def load_config(config_path: Path | str = DEFAULT_CONFIG_PATH) -> Settings:
    """Memuat konfigurasi aplikasi dari berkas dan environment variable."""

    parser = ConfigParser()
    path = Path(config_path)
    if path.exists():
        parser.read(path)

    frista_path = _read_value(parser, "Frista", "path", fallback=r"D:\\BPJS\\Frista\\Frista.exe")
    frista_settings = ApplicationSettings(
        path=frista_path,
        username=_read_value(parser, "Frista", "username", fallback=""),
        password=_read_value(
            parser,
            "Frista",
            "password",
            fallback="",
            env_key="FRISTA_PASSWORD",
        ),
        window_title=_read_value(
            parser,
            "Frista",
            "window_title",
            fallback="Frista (Face Recognition BPJS Kesehatan)",
        ),
        launch_delay=_read_float(parser, "Frista", "launch_delay", fallback=5.0),
        submit_key=_read_value(parser, "Frista", "submit_key", fallback="space"),
        working_dir=_read_optional(parser, "Frista", "working_dir")
        or str(Path(frista_path).parent),
    )

    after_path = _read_value(
        parser,
        "After",
        "path",
        fallback=r"C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe",
    )
    after_settings = ApplicationSettings(
        path=after_path,
        username=_read_value(parser, "After", "username", fallback=""),
        password=_read_value(parser, "After", "password", fallback="", env_key="AFTER_PASSWORD"),
        window_title=_read_value(parser, "After", "window_title", fallback="After"),
        launch_delay=_read_float(parser, "After", "launch_delay", fallback=7.0),
        submit_key=_read_value(parser, "After", "submit_key", fallback="enter"),
        working_dir=_read_optional(parser, "After", "working_dir")
        or str(Path(after_path).parent),
    )

    camera_settings = CameraSettings(
        camera_id=_read_int(parser, "Camera", "camera_id", fallback=0),
        api=_read_value(parser, "Camera", "api", fallback="https://frista.bpjs-kesehatan.go.id/frista-api"),
    )

    workflow_settings = WorkflowSettings(
        post_login_delay=_read_float(parser, "Workflow", "post_login_delay", fallback=1.0),
        network_timeout=_read_float(parser, "Workflow", "network_timeout", fallback=5.0),
    )

    return Settings(
        frista=frista_settings,
        after=after_settings,
        camera=camera_settings,
        workflow=workflow_settings,
    )


__all__ = [
    "ApplicationSettings",
    "CameraSettings",
    "WorkflowSettings",
    "Settings",
    "load_config",
]
