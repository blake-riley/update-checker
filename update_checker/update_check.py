#!/usr/bin/env python

"""Check repos for updated versions."""

import sys
from argparse import ArgumentParser
from typing import Optional

from . import configuration, globalvars


def check_for_updates(config_filename: Optional[str]) -> None:
    """Check for updates."""
    config = configuration.get_config(config_filename)

    error_code = False
    error_strings = []
    for package in config.tracked_packages:
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
    globalvars.OPTIONS |= options.__dict__
    check_for_updates(options.config_filename)


if __name__ == "__main__":
    _entrypoint()
