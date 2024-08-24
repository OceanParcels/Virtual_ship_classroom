"""Schedule class."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict

from .waypoint import Waypoint


class Schedule(BaseModel):
    """Schedule of the virtual ship."""

    waypoints: list[Waypoint]

    model_config = ConfigDict(extra="forbid")

    def to_yaml(self, file_path: str | Path) -> None:
        """
        Write schedule to yaml file.

        :param file_path: Path to the file to write to.
        """
        with open(file_path, "w") as file:
            yaml.dump(
                self.model_dump(
                    by_alias=True,
                ),
                file,
            )

    @classmethod
    def from_yaml(cls, file_path: str | Path) -> Schedule:
        """
        Load schedule from yaml file.

        :param file_path: Path to the file to load from.
        :returns: The schedule.
        """
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return Schedule(**data)