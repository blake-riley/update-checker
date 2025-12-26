"""Parse a config file."""

import os
import pathlib
from functools import cached_property
from typing import Any, Deque, Optional

import yaml
from pydantic.dataclasses import dataclass

from . import globalvars, trackers


@dataclass
class Config:
    """Defines the schema for a config file."""

    packages: list[dict[str, str]]
    config_filepath: Optional[str] = None

    @cached_property
    def tracked_packages(self) -> list[trackers.PackageTracker]:
        """Return a list of Package objects."""
        tracked_packages = []
        for pkg in self.packages:
            try:
                source = pkg["source"]
                Tracker = trackers.get_tracker(source)
            except ValueError as e:
                raise ValueError(f"Error building tracker for {pkg}") from e
            else:
                tracked_packages.append(Tracker(**pkg))  # type: ignore[call-arg]

        return tracked_packages


def parse_config(unvalidated_config: dict[str, Any], config_filepath: str) -> Config:
    """Parse a config file."""
    config = Config(
        **unvalidated_config,
        config_filepath=config_filepath,
    )  # type: ignore[call-arg]

    return config


def get_config(config_filename: Optional[str]) -> Config:
    """Read the config file and returns a dictionary of the config."""
    if not config_filename:
        config_filename = "tracked_packages.yml"

    search_paths = Deque(
        [
            pathlib.Path(".") / config_filename,
            pathlib.Path.home() / ".config" / "update-checker" / config_filename,
            pathlib.Path(__file__).parent.parent / config_filename,
        ]
    )
    config_path = pathlib.Path(config_filename)
    if config_path.is_absolute():
        search_paths.appendleft(config_path)
    env_config_path = os.environ.get("UPDATE_CHECKER_CONFIG_FILE")
    if env_config_path:
        search_paths.appendleft(pathlib.Path(env_config_path))

    for config_path in search_paths:
        try:
            with open(config_path, "r") as f:
                unvalidated_config: dict[str, Any] = yaml.load(
                    f, Loader=yaml.SafeLoader
                )
                config = parse_config(unvalidated_config, config_path.as_posix())
        except IOError:
            pass
        else:
            if globalvars.OPTIONS["verbose"]:
                print(config.config_filepath)
            return config

    raise FileNotFoundError(
        f"Could not find a config file with name: {config_filename}!"
    )
