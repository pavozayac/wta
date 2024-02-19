import datetime
from pydantic import BaseModel, computed_field, field_validator

from wta.api.stops.models import StopLocation


class ScheduledBusStop(StopLocation):
    brigade: str
    time: datetime.time

    # @field_validator('time')
    # def convert_24th_hour(cls, v: str):
    #     if v.split(':')[0] == '24':
    #         return '00:00:00'
    #     else:
    #         return v

    @computed_field
    @property
    def timestamp(self) -> float:
        today = datetime.datetime.now()

        time = datetime.datetime(
            year=today.year, 
            month=today.month, 
            day=today.day, 
            hour=self.time.hour, 
            minute=self.time.minute, 
            second=self.time.second
        )

        return time.timestamp()




class BrigadeSchedule(BaseModel):
    brigade: str
    stops: list[ScheduledBusStop]


class LineSchedule(BaseModel):
    line: str
    brigades: dict[str, BrigadeSchedule]


class CompleteSchedule(BaseModel):
    lines: dict[str, LineSchedule]
