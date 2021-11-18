#!/usr/bin/env python

"""Check repos for updated versions."""

import os
import pathlib
import sys
from argparse import ArgumentParser, Namespace
from typing import Any, Deque, Optional

import yaml

from .config import parse_config


def get_config(config_filename: Optional[str]) -> dict[str, Any]:
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
                config: dict[str, Any] = yaml.load(f, Loader=yaml.SafeLoader)
                return config
        except IOError:
            pass

    raise FileNotFoundError(
        f"Could not find a config file with name: {config_filename}!"
    )


def check_for_updates(config_filename: Optional[str], opts: Namespace) -> None:
    """Check for updates."""
    config = get_config(config_filename)
    if opts.verbose:
        print(config)

    tracked_packages = parse_config(config)

    error_code = False
    error_strings = []
    for package in tracked_packages:
        if not package.is_latest_release():
            error_strings.append(
                f"{package} is out of date! "
                f"({package.latest_release} != {package.current_tag})"
            )
            error_code = True

    if error_code:
        print("\n".join(error_strings), file=sys.stderr)
        sys.exit(1)


def _entrypoint() -> None:
    """Entrypoint for the update-checker script."""
    parser = ArgumentParser()
    parser.add_argument("config_filename", nargs="?", help="yaml config file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print more info")
    options = parser.parse_args()
    check_for_updates(options.config_filename, options)


if __name__ == "__main__":
    _entrypoint()
