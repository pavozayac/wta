from pydantic import BaseModel, Field, computed_field
from datetime import datetime
from typing import List


class BusLocation(BaseModel):
    Lat: float
    Lon: float
    Time: datetime
    Lines: str
    VehicleNumber: str
    Brigade: str

    @computed_field
    @property
    def Timestamp(self) -> float:
        return self.Time.timestamp()


class BusLocationResponse(BaseModel):
    locations: list[BusLocation] | str = Field(
        ..., alias='result')


class BusLocationList(BaseModel):
    locations: list[BusLocation]
