import datetime
from pydantic import BaseModel

from wta.api.stops.models import StopLocation


class ScheduledBusStop(StopLocation):
    brigade: str
    # line: str
    # lon: float
    # lat: float
    time: datetime.time


class BrigadeSchedule(BaseModel):
    brigade: str
    stops: list[ScheduledBusStop]


class LineSchedule(BaseModel):
    line: str
    brigades: dict[str, BrigadeSchedule]


class CompleteSchedule(BaseModel):
    lines: dict[str, LineSchedule]
