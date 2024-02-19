import datetime
from pydantic import BaseModel


# TODO: move this to models in wta.api.stops
class BusStop(BaseModel):
    bus_stop_group_nr: str
    bus_stop_nr: str
    # does the line need to be here, for now maybe not
    # line: str
    lon: float
    lat: float


class ScheduledBusStop(BusStop):
    brigade: str
    line: str
    lon: float
    lat: float
    time: datetime.time


class BrigadeSchedule(BaseModel):
    brigade: str
    stops: list[ScheduledBusStop]


class LineSchedule(BaseModel):
    line: str
    brigades: dict[str, BrigadeSchedule]


class CompleteSchedule(BaseModel):
    lines: dict[str, LineSchedule]
