from datetime import datetime, timedelta

import pyproj

from virtualship import Location
from virtualship.expedition import Schedule, ShipConfig, Waypoint
from virtualship.expedition.simulate_schedule import (
    ScheduleOk,
    ScheduleProblem,
    simulate_schedule,
)


def test_simulate_schedule_feasible() -> None:
    """Test schedule with two waypoints that can be reached within time is OK."""
    base_time = datetime.strptime("2022-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")

    projection = pyproj.Geod(ellps="WGS84")
    ship_config = ShipConfig.from_yaml("expedition_dir/ship_config.yaml")
    ship_config.ship_speed_meter_per_second = 5.14
    schedule = Schedule(
        waypoints=[
            Waypoint(Location(0, 0), base_time),
            Waypoint(Location(0.01, 0), base_time + timedelta(days=1)),
        ]
    )

    result = simulate_schedule(projection, ship_config, schedule)

    assert isinstance(result, ScheduleOk)


def test_simulate_schedule_too_far() -> None:
    """Test schedule with two waypoints that are very far away and cannot be reached in time is not OK."""
    base_time = datetime.strptime("2022-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")

    projection = pyproj.Geod(ellps="WGS84")
    ship_config = ShipConfig.from_yaml("expedition_dir/ship_config.yaml")
    schedule = Schedule(
        waypoints=[
            Waypoint(Location(0, 0), base_time),
            Waypoint(Location(1.0, 0), base_time + timedelta(minutes=1)),
        ]
    )

    result = simulate_schedule(projection, ship_config, schedule)

    assert isinstance(result, ScheduleProblem)
