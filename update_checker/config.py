"""Parse a config file."""

from typing import Any
from pydantic import BaseModel

from . import trackers


class Config(BaseModel):
    """Defines the schema for a config."""

    packages: list[dict[str, str]]


def parse_config(unvalidated_config: dict[str, Any]) -> list[trackers.PackageTracker]:
    """Parse the config and return a list of package tracker objects."""
    config = Config(**unvalidated_config)

    packages = []
    for pkg in config.packages:
        try:
            source = pkg['source']
            Tracker = trackers.get_tracker(source)
        except ValueError as e:
            raise ValueError(f'Error building tracker for {pkg}') from e
        else:
            packages.append(Tracker(**pkg))  # type: ignore[call-arg]

    return packages
