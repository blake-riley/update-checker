"""Trackers for getting the current version."""

from abc import abstractmethod
from dataclasses import field
from functools import cached_property
from typing import Literal, Type

import requests
from pydantic.dataclasses import dataclass


class PackageTracker:
    """Interface for tracker classes."""

    source: str = NotImplemented
    current_tag: str = NotImplemented

    @abstractmethod
    def latest_release(self) -> str:
        """Get the latest online release version."""
        ...

    @abstractmethod
    def is_latest_release(self) -> bool:
        """Check that the version listed is the latest release available online."""
        ...


@dataclass
class GithubPackageTracker(PackageTracker):
    """Get package information from Github."""

    owner: str = field()
    repo: str = field()
    current_tag: str = field()
    allow_prerelease: bool = field(default=False)
    source: Literal["github"] = "github"

    @cached_property
    def latest_release(self) -> str:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases"

        r = requests.get(
            url,
            params={
                "accept": "application/vnd.github.v3+json",
            },
        )
        r.raise_for_status()

        version_list = list(r.json())
        if not self.allow_prerelease:
            # Filter out the prereleases
            version_list = list(filter(lambda rel: not rel["prerelease"], version_list))

        latest_release = str(version_list[0].get("name") or "")
        return latest_release

    def is_latest_release(self) -> bool:
        return self.latest_release == self.current_tag

    def __str__(self) -> str:
        return f"{self.owner}/{self.repo}"


def get_tracker(tracker_name: str) -> Type[PackageTracker]:
    """Return a tracker based on the name provided."""
    all_trackers = {
        tracker.source: tracker for tracker in PackageTracker.__subclasses__()
    }

    tracker = all_trackers.get(tracker_name)
    if not tracker:
        raise ValueError(f"No tracker found for {tracker_name}")

    return tracker
