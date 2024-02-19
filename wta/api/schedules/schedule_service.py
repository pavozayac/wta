from abc import ABC, abstractmethod
from datetime import datetime
import requests
from urllib.parse import urljoin
from http import HTTPStatus

from wta.api.generic.access_service import ApiAccessService
from wta.api.generic.models import GenericKVResponse

from wta.api.routes.models import RouteStop
from wta.api.schedules.models import BrigadeSchedule, BusStop, LineSchedule, ScheduledBusStop


class ScheduleService(ABC):

    @abstractmethod
    def get_stop_schedule(self, stop_nr: str, stop_group_nr: str) -> GenericKVResponse:
        pass

    @abstractmethod
    def get_schedule(self, line_stops: dict[str, RouteStop]):
        pass


class ApiScheduleService(ScheduleService):

    def __init__(
            self,
            access_service: ApiAccessService,
            path='action/dbtimetable_get/',
            id='e923fa0e-d96c-43f9-ae6e-60518c9f3238') -> None:
        self.access_service = access_service
        self.url_path = path
        self.id = id

    def get_stop_schedule(self, line: str, stop_nr: str, stop_group_nr: str) -> GenericKVResponse:
        query_params = {
            'apikey': self.access_service.api_key(),
            'id': self.id,
            'line': line,
            'busstopId': stop_group_nr,
            'busstopNr': stop_nr,
        }

        req_url = urljoin(self.access_service.base_api_url(), self.url_path)

        response = requests.get(
            req_url, params=query_params, timeout=1000)

        if response.status_code != HTTPStatus.OK or 'result' not in response.json():
            raise ConnectionError(
                f'Server returned error response {response.status_code} at {response.url}. \n')

        parsed = GenericKVResponse(**response.json())

        return parsed

    # TODO: maybe get the full list of stops as an argument here to not reload it without need
    def get_line_schedule(self, line: str, line_stops: list[BusStop]) -> LineSchedule:
        brigades: dict[str, BrigadeSchedule] = {}

        for stop in line_stops:
            stop_schedule = self.get_stop_schedule(line, stop.bus_stop_nr, stop.bus_stop_group_nr)

            time = datetime.utcnow().time()
            brigade = ''

            for key_value_list in stop_schedule.result:
                for key_value in key_value_list.values:
                    if key_value.key == 'brygada':
                        brigade = key_value.value

                    if key_value.key == 'czas':
                        time = key_value.value

                # get from another service
                # stop = ...

                brigades[brigade] = BrigadeSchedule(
                    brigade=brigade, stops=brigades.get(
                        brigade, BrigadeSchedule(
                            # TODO: put the stop into this list
                            brigade=brigade, stops=[])).stops + [])

        return LineSchedule(line=line, brigades=brigades)
