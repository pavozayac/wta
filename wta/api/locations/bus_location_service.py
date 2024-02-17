from abc import ABC, abstractmethod
from http import HTTPStatus
from urllib.parse import urljoin
from pydantic import ValidationError

import requests

from wta.exceptions.undef_server_behaviour import UndefinedServerBehaviourError

from .models import BusLocation, BusLocationResponse
from ..access_service import ApiAccessService


class BusLocationService(ABC):

    @abstractmethod
    def get_bus_locations(self, api_access: ApiAccessService) -> list[BusLocation]:
        pass


class ApiBusLocationService(BusLocationService):

    # Perhaps change this to an environment variable?
    def __init__(self,
                 path='action/busestrams_get/',
                 resource_id='f2e5503e-927d-4ad3-9500-4ab9e55deb59') -> None:

        self.locations_path = path
        self.resource_id = resource_id

    def get_bus_locations(self, api_access: ApiAccessService) -> list[BusLocation]:

        query_params = {
            'apikey': api_access.api_key(),
            'type': 1,
            'resource_id': self.resource_id,

        }

        req_url = urljoin(api_access.base_api_url(), self.locations_path)

        response = requests.get(
            req_url, params=query_params, timeout=1000)

        if response.status_code != HTTPStatus.OK or 'result' not in response.json():
            raise ConnectionError(
                f'Server returned error response {response.status_code} at {response.url}. \n')


        while True:
            try:
                body = BusLocationResponse(**response.json())
                break
            except ValidationError:
                pass
                

        if isinstance(body.locations, str):
            raise UndefinedServerBehaviourError(
                f'Server returned undescribed error response. \n')

        return body.locations
