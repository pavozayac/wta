from abc import ABC, abstractmethod
from urllib.parse import urljoin
import requests
from http import HTTPStatus

from wta.api.access_service import ApiAccessService, EnvApiAccessService
from wta.api.routes.models import RouteResponse

from wta.api.schedules.models import BusStop


class RouteService(ABC):

    @abstractmethod
    def get_routes(self, line: str) -> dict[str, list[BusStop]]:
        pass


class ApiRouteService(RouteService):

    def __init__(self, access_service: ApiAccessService,
                 path='action/public_transport_routes/') -> None:
        self.access_service = access_service
        self.url_path = path

    @staticmethod
    def __reorganize_stops(response: RouteResponse) -> dict[str, list[BusStop]]:
        reorganized: dict[str, list[BusStop]] = {}

        for k, directions in response.result.items():
            stops = []

            for dir in directions.values():
                stops.extend(dir.values())

            reorganized[k] = reorganized.get(k, []) + stops

        return reorganized

    def get_routes(self) -> dict[str, list[BusStop]]:
        query_params = {
            'apikey': self.access_service.api_key(),
        }

        req_url = urljoin(self.access_service.base_api_url(), self.url_path)

        response = requests.get(
            req_url, params=query_params, timeout=1000)

        if response.status_code != HTTPStatus.OK or 'result' not in response.json():
            raise ConnectionError(
                f'Server returned error response {response.status_code} at {response.url}. \n')

        parsed = RouteResponse(**response.json())

        reorganized = ApiRouteService.__reorganize_stops(parsed)

        return reorganized


if __name__ == '__main__':
    serv = ApiRouteService(EnvApiAccessService())

    routes = serv.get_routes()

    print(routes['L51'])
