from abc import ABC, abstractmethod
from http import HTTPStatus
import requests

from .model import BusLocation, BusLocationList
from ..access_service import ApiAccessService


class BusLocationService(ABC):

    @abstractmethod
    def get_bus_locations(self, api_access: ApiAccessService) -> list[BusLocation]:
        pass


class ApiBusLocationService(BusLocationService):

    # Perhaps change this to an environment variable?
    def __init__(self,
                 url='https://api.um.warszawa.pl/api/action/busestrams_get/',
                 resource_id='f2e5503e-927d-4ad3-9500-4ab9e55deb59') -> None:

        self.locations_url = url
        self.resource_id = resource_id

    def get_bus_locations(self, api_access: ApiAccessService) -> list[BusLocation]:

        query_params = {
            'apikey': api_access.api_key(),
            'type': 1,
            'resource_id': self.resource_id,

        }

        response = requests.get(
            self.locations_url, params=query_params, timeout=1000)

        if response.status_code != HTTPStatus.OK:
            raise ConnectionError('Server returned error response.')

        body = BusLocationList(**response.json())

        return body.locations
