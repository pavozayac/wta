from abc import ABC, abstractmethod
from json import dump, dumps, load
import os
import time

import pydantic

from pydantic import json as pydjson


# from ..api.buses.models import BusLocation, BusLocationList, SaveBusData
from wta.api.locations.models import BusLocationList
from wta.api.schedules.models import CompleteSchedule
from wta.storage.models import SaveBusData, BusHistory


class CompleteScheduleRepository(ABC):

    # @abstractmethod
    # def get_bus_history(self) -> BusHistory:
    #     pass

    @abstractmethod
    def get_schedule(self, file_path: str) -> CompleteSchedule:
        pass

    @abstractmethod
    def save_schedule(self, schedule: CompleteSchedule):
        pass


class JSONScheduleRepository(CompleteScheduleRepository):

    def __init__(self, file_path: str = './out/schedule.json') -> None:
        self.file_path = file_path
        pass

    def get_schedule(self) -> CompleteSchedule:
        complete_schedule = CompleteSchedule(lines={})

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as json_file:
                return CompleteSchedule(**load(json_file))

        return complete_schedule

        

    def save_schedule(self, schedule: CompleteSchedule):
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        
        with open(self.file_path, 'w') as json_file:
            json_file.write(schedule.model_dump_json())

