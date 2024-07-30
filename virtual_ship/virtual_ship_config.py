"""VirtualShipConfig class."""

from dataclasses import dataclass

from parcels import FieldSet

from .location import Location
from .waypoint import Waypoint


@dataclass
class ArgoFloatConfig:
    """Configuration for argos floats."""

    fieldset: FieldSet
    max_depth: float
    drift_depth: float
    vertical_speed: float
    cycle_days: float
    drift_days: float


@dataclass
class ADCPConfig:
    """Configuration for ADCP instrument."""

    max_depth: float
    bin_size_m: int


@dataclass
class VirtualShipConfig:
    """Configuration of the virtual ship."""

    ship_speed: float  # m/s

    waypoints: list[Waypoint]

    adcp_fieldset: FieldSet
    ship_underwater_st_fieldset: FieldSet
    ctd_fieldset: FieldSet
    drifter_fieldset: FieldSet

    argo_float_config: ArgoFloatConfig
    adcp_config: ADCPConfig

    def verify(self) -> None:
        """
        Verify this configuration is valid.

        :raises ValueError: If not valid.
        """
        if len(self.waypoints) < 2:
            raise ValueError("Waypoints require at least a start and an end.")

        if not all(
            [self._is_valid_location(waypoint.location) for waypoint in self.waypoints]
        ):
            raise ValueError("Invalid location for waypoint.")

        if self.argo_float_config.max_depth > 0:
            raise ValueError("Argo float max depth must be negative or zero.")

        if self.argo_float_config.drift_depth > 0:
            raise ValueError("Argo float drift depth must be negative or zero.")

        if self.argo_float_config.vertical_speed >= 0:
            raise ValueError("Argo float vertical speed must be negative.")

        if self.argo_float_config.cycle_days <= 0:
            raise ValueError("Argo float cycle days must be larger than zero.")

        if self.argo_float_config.drift_days <= 0:
            raise ValueError("Argo drift cycle days must be larger than zero.")

        if self.adcp_config.max_depth > 0:
            raise ValueError("ADCP max depth must be negative.")

    @staticmethod
    def _is_valid_location(location: Location) -> bool:
        return (
            location.lat >= -90
            and location.lat <= 90
            and location.lon >= -180
            and location.lon <= 360
        )