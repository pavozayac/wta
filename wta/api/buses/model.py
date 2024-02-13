from pydantic import BaseModel, Field
from datetime import datetime


class BusLocation(BaseModel):
    latitude: float = Field(alias='Lat')
    longitude: float = Field(alias='Lon')
    time: datetime = Field(alias='Time')
    line: str = Field(alias='Lines')
    vehicle_number: str = Field(alias='VehicleNumber')
    brigade: str = Field(alias='Brigade')


class BusLocationList(BaseModel):
    locations: list[BusLocation] = Field(alias='result')
