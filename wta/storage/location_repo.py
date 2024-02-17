from abc import ABC, abstractmethod
from json import dump, dumps, load
import os
import time

import pydantic

from pydantic import json as pydjson


# from ..api.buses.models import BusLocation, BusLocationList, SaveBusData
from wta.api.locations.models import BusLocationList
from wta.storage.models import SaveBusData, BusHistory


class LocationRepository(ABC):

    # @abstractmethod
    # def get_bus_history(self) -> BusHistory:
    #     pass

    @abstractmethod
    def get_locations(self, file_path: str) -> BusLocationList:
        pass

    @abstractmethod
    def save_locations(self, locations_list: BusLocationList, file_path: str):
        pass


class JSONFileLocationRepository(LocationRepository):

    def __init__(self) -> None:
        # self.file_path = file_path
        pass

    # def get_bus_history(self, vehicle_number: str) -> BusHistory | None:
    #     if os.path.exists(self.file_path):
    #         with open(self.file_path, 'r') as json_file:
    #             saved_bus_dict = SaveBusData(**load(json_file))

    #             return saved_bus_dict.bus_histories.get(vehicle_number, None)

    #     return None

    def get_locations(self, file_path: str) -> SaveBusData:
        saved_data = SaveBusData(bus_dict={})

        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                saved_data = SaveBusData(**load(json_file))

        return saved_data

    @staticmethod
    def __convert_list_to_bus_dicts(loc_list: BusLocationList) -> SaveBusData:
        bus_dict: dict[str, BusHistory] = dict()

        for bl in loc_list.locations:
            if bl.VehicleNumber not in bus_dict:
                bus_dict[bl.VehicleNumber] = BusHistory(
                    vehicle_number=bl.VehicleNumber, times={bl.Time: bl})
            else:
                bus_dict[bl.VehicleNumber].times |= {bl.Time: bl}

        return SaveBusData(bus_dict=bus_dict)

    @staticmethod
    def __merge_bus_histories(a: SaveBusData, b: SaveBusData) -> SaveBusData:
        new_histories = a.bus_dict | b.bus_dict

        for k, v in a.bus_dict.items():
            new_histories[k] = BusHistory(
                vehicle_number=k,
                times=v.times | b.bus_dict.get(k, BusHistory(vehicle_number=k, times={})).times)

        return SaveBusData(bus_dict=new_histories)

    def save_locations(self, locations_list: BusLocationList, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        saved_data = self.get_locations(file_path)

        new_data = JSONFileLocationRepository.__convert_list_to_bus_dicts(
            locations_list)

        combined = JSONFileLocationRepository.__merge_bus_histories(
            saved_data, new_data)

        # combined = JSONFileLocationRepository.__merge_bus_histories(saved)

        with open(file_path, 'w') as json_file:
            json_file.write(combined.model_dump_json())
