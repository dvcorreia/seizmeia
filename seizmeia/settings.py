from __future__ import annotations

from enum import Enum
from ipaddress import IPv4Address
from os import path
from pathlib import Path
from typing import Union, Any
from collections.abc import Iterable

import yaml
from pydantic import BaseModel, BaseSettings, DirectoryPath, Field
from pydantic.env_settings import SettingsSourceCallable

from seizmeia.user.config import Config as AuthConfig


class EnvironmentSettings(str, Enum):
    DEV = "development"
    PROD = "production"

    def is_dev(self) -> bool:
        return self.value == "development"


class UvicornSettings(BaseModel):
    port: int = 80
    host: IPv4Address = IPv4Address("0.0.0.0")
    workers: int = 1


FileName = Path | str
DirectoryPaths = Union[
    DirectoryPath, list[DirectoryPath | str], tuple[DirectoryPath | str, ...]
]


def yaml_settings(
    file_name: FileName, dirs: DirectoryPaths
) -> SettingsSourceCallable:
    """Source for loading yaml configuration files"""

    def load_settings(settings: BaseSettings) -> dict[str, Any]:
        file_path = _search_file(file_name, dirs)

        if not file_path:
            return {}

        with open(file_path, encoding="utf-8") as reader:
            config: dict[str, Any] = yaml.safe_load(reader)

        return config

    return load_settings


def _search_file(file_name: FileName, dirs: DirectoryPaths) -> Path | None:
    """Searches for file in directories"""
    if not isinstance(dirs, Iterable):
        dirs = [dirs]

    for directory in dirs:
        if not path.isdir(directory):
            continue

        file_path = Path(path.join(directory, file_name))

        if path.exists(file_path) and path.isfile(file_path):
            return file_path

    return None


class Settings(BaseSettings):
    """Defines the configuration of Seizmeia"""

    environment: EnvironmentSettings = EnvironmentSettings.PROD
    uvicorn: UvicornSettings = Field(default_factory=UvicornSettings)
    database_url: str = "sqlite:///"
    auth: AuthConfig = Field(default_factory=AuthConfig)

    class Config:
        env_prefix = "seizmeia_"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                env_settings,
                yaml_settings(
                    file_name="seizmeia.yml",
                    dirs=(".", "/etc/seizmeia", Path.home()),
                ),
                init_settings,
                file_secret_settings,
            )


config = Settings()

if __name__ == "__main__":
    import sys

    sys.stdout.write(config.json())
    sys.exit(0)
