from abc import ABC, abstractmethod
from json import dump, dumps, load
import os
import time

import pydantic

from pydantic import json as pydjson


# from ..api.buses.models import BusLocation, BusLocationList, SaveBusData
from wta.api.buses.models import BusLocationList
from wta.storage.models import SaveBusData, BusHistory


class LocationRepository(ABC):

    # @abstractmethod
    # def get_bus_history(self) -> BusHistory:
    #     pass

    @abstractmethod
    def get_locations(self) -> BusLocationList:
        pass

    @abstractmethod
    def save_locations(self, locations_list: BusLocationList) -> None:
        pass


class JSONFileLocationRepository(LocationRepository):

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    # def get_bus_history(self, vehicle_number: str) -> BusHistory | None:
    #     if os.path.exists(self.file_path):
    #         with open(self.file_path, 'r') as json_file:
    #             saved_bus_dict = SaveBusData(**load(json_file))

    #             return saved_bus_dict.bus_histories.get(vehicle_number, None)

    #     return None

    def get_locations(self) -> BusLocationList:
        saved_data = BusLocationList(locations=[])

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as json_file:
                saved_data = BusLocationList(**load(json_file))

        return saved_data

    # @staticmethod
    # def __convert_list_to_bus_dicts(locations: list[BusLocation]) -> SaveBusData:
    #     bus_dict: dict[str, BusHistory] = dict()

    #     for bl in locations:
    #         if bl.vehicle_number not in bus_dict:
    #             bus_dict[bl.vehicle_number] = BusHistory(
    #                 vehicle_number=bl.vehicle_number, times={bl.time: bl})
    #         else:
    #             bus_dict[bl.vehicle_number].times |= {bl.time: bl}

    #     return SaveBusData(bus_histories=bus_dict)

    # @staticmethod
    # def __merge_bus_histories(a: SaveBusData, b: SaveBusData) -> SaveBusData:
    #     new_histories = a.bus_histories | b.bus_histories

    #     for k, v in a.bus_histories.items():
    #         new_histories[k] = BusHistory(
    #             vehicle_number=k,
    #             times=v.times | b.bus_histories.get(k, BusHistory(vehicle_number=k, times={})).times)

    #     return SaveBusData(bus_histories=new_histories)

    def save_locations(self, locations_list: BusLocationList) -> None:
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        saved_data = self.get_locations()

        # new_data_dict = JSONFileLocationRepository.__convert_list_to_bus_dicts(
        #     locations)

        # new_saved_bus = JSONFileLocationRepository.__merge_bus_histories(
        #     saved_bus_dict, new_data_dict)

        combined = BusLocationList(
            locations=saved_data.locations + locations_list.locations)

        with open(self.file_path, 'w') as json_file:
            # dump(combined.model_dump(), json_file)
            json_file.write(combined.model_dump_json())
