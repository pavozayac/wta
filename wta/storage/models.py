from datetime import datetime
from pydantic import BaseModel

from wta.api.buses.models import BusLocation


class BusHistory(BaseModel):
    vehicle_number: str
    times: dict[datetime, BusLocation]


class SaveBusData(BaseModel):
    bus_dict: dict[str, BusHistory]
