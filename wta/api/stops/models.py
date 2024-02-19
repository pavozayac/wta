from pydantic import BaseModel


class StopInfo(BaseModel):
    stop_group_nr: str
    stop_nr: str


class StopLocation(StopInfo):
    lon: float
    lat: float
