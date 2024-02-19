from abc import ABC, abstractmethod
from http import HTTPStatus
from urllib.parse import urljoin
import requests

from wta.api.generic.models import GenericKVResponse
from wta.api.generic.access_service import ApiAccessService, EnvApiAccessService


class StopLocationService(ABC):

    @abstractmethod
    def get_stop_locations(self) -> GenericKVResponse:
        pass


class ApiStopLocationService(StopLocationService):

    def __init__(self,
                 access_service: ApiAccessService,
                 path='action/dbstore_get/',
                 id='ab75c33d-3a26-4342-b36a-6e5fef0a3ac3') -> None:

        self.access_service = access_service
        self.url_path = path
        self.id = id

    def get_stop_locations(self) -> GenericKVResponse:

        query_params = {
            'apikey': self.access_service.api_key(),
            'id': self.id,

        }

        req_url = urljoin(self.access_service.base_api_url(), self.url_path)

        response = requests.get(
            req_url, params=query_params, timeout=1000)

        if response.status_code != HTTPStatus.OK or 'result' not in response.json():
            raise ConnectionError(
                f'Server returned error response {response.status_code} at {response.url}. \n')

        parsed = GenericKVResponse(**response.json())

        # TODO: change return type and add some conversion into a more appropriate
        # and useful form, like a dict[str, dict[str, StopLocation]],
        # so a dict from stop group nr, to a dict from stop nr to a stop location

        return parsed


if __name__ == '__main__':
    loc_serv = ApiStopLocationService(EnvApiAccessService())

    print(loc_serv.get_stop_locations())
