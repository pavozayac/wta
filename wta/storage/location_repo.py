from abc import ABC, abstractmethod
from json import load, dump


from ..api.buses.models import BusLocation, BusLocationList


class LocationRepository(ABC):

    def get_locations(self) -> list[BusLocation]:
        pass

    def save_locations(self, locations: list[BusLocation]) -> None:
        pass


class JSONFileLocationRepository(LocationRepository):

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_locations(self) -> list[BusLocation]:
        with open(self.file_path, 'r') as json_file:

            bl_list = BusLocationList(**load(json_file))

            return bl_list.locations

    def save_locations(self, locations: list[BusLocation]) -> None:
        with open(self.file_path, 'w') as json_file:

            bllist = BusLocationList(result=locations)

            dump(bllist, json_file)
