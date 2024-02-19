from abc import ABC, abstractmethod
from http import HTTPStatus
from urllib.parse import urljoin
import requests

from wta.api.generic.models import GenericKVResponse
from wta.api.generic.access_service import ApiAccessService, EnvApiAccessService
from wta.api.stops.models import StopLocation


class StopLocationService(ABC):

    @abstractmethod
    def get_stop_locations(self) -> dict[str, dict[str, StopLocation]]:
        pass


class ApiStopLocationService(StopLocationService):

    def __init__(self,
                 access_service: ApiAccessService,
                 path='action/dbstore_get/',
                 id='ab75c33d-3a26-4342-b36a-6e5fef0a3ac3') -> None:

        self.access_service = access_service
        self.url_path = path
        self.id = id

    @staticmethod
    def __convert_to_dict(response: GenericKVResponse) -> dict[str, dict[str, StopLocation]]:
        converted: dict[str, dict[str, StopLocation]] = {}

        for kvlist in response.result:
            props = {}

            for kv in kvlist.values:
                match kv.key:
                    case 'zespol':
                        props |= {'stop_group_nr': kv.value}
                    case 'slupek':
                        props |= {'stop_nr': kv.value}
                    case 'dlug_geo':
                        props |= {'lon': kv.value}
                    case 'szer_geo':
                        props |= {'lat': kv.value}

            converted[props['stop_group_nr']] = converted.get(props['stop_group_nr'], {}) | {
                props['stop_nr']: StopLocation(**props)}

        return converted

    def get_stop_locations(self) -> dict[str, dict[str, StopLocation]]:
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

        converted = ApiStopLocationService.__convert_to_dict(parsed)

        return converted


if __name__ == '__main__':
    loc_serv = ApiStopLocationService(EnvApiAccessService())

    print(loc_serv.get_stop_locations())
