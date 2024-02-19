from abc import ABC, abstractmethod
from datetime import datetime
import requests
from urllib.parse import urljoin
from http import HTTPStatus

from wta.api.generic.access_service import ApiAccessService, EnvApiAccessService
from wta.api.generic.models import GenericKVResponse

from wta.api.routes.models import RouteStop
from wta.api.routes.route_service import ApiRouteService
from wta.api.schedules.models import BrigadeSchedule, CompleteSchedule, LineSchedule, ScheduledBusStop
from wta.api.stops.models import StopInfo, StopLocation
from wta.api.stops.stop_loc_service import ApiStopLocationService
from wta.storage.full_schedule_repo import JSONScheduleRepository


class ScheduleService(ABC):

    @abstractmethod
    def get_stop_schedule(self, stop_nr: str, stop_group_nr: str) -> GenericKVResponse:
        pass

    @abstractmethod
    def get_full_schedules(self,
                           routes: dict[str, list[StopInfo]],
                           all_stops: dict[str,
                                           dict[str,
                                                StopLocation]]) -> CompleteSchedule:
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
            req_url, params=query_params, timeout=10)

        if response.status_code != HTTPStatus.OK or 'result' not in response.json():
            raise ConnectionError(
                f'Server returned error response {response.status_code} at {response.url}. \n')

        parsed = GenericKVResponse(**response.json())

        return parsed

    def __create_line_schedule(self,
                               line: str,
                               stop_infos: list[StopInfo],
                               all_stops: dict[str,
                                               dict[str,
                                                    StopLocation]]) -> LineSchedule:
        brigades: dict[str, BrigadeSchedule] = {}

        for stop_info in stop_infos:
            stop_schedule = self.get_stop_schedule(line, stop_info.stop_nr, stop_info.stop_group_nr)

            time = datetime.utcnow().time()
            brigade = ''

            for key_value_list in stop_schedule.result:
                # bad_time = False

                for key_value in key_value_list.values:
                    if key_value.key == 'brygada':
                        brigade = key_value.value

                    if key_value.key == 'czas':
                        h, m, s = key_value.value.split(':')

                        if int(h) >= 24:
                            h = str(int(h) % 24).zfill(2)

                        time = f'{h}:{m}:{s}'

                stop_location = all_stops[stop_info.stop_group_nr][stop_info.stop_nr]

                scheduled_stop = ScheduledBusStop(**{
                    **stop_location.model_dump(),
                    'time': time,
                    'brigade': brigade
                })

                brig = brigades.get(brigade, BrigadeSchedule(brigade=brigade, stops=[]))

                brig.stops.append(scheduled_stop)

                brigades[brigade] = brig

                # brigades[brigade] = BrigadeSchedule(
                #     brigade=brigade, stops=brigades.get(
                #         brigade, BrigadeSchedule(
                #             brigade=brigade, stops=[])).stops + [scheduled_stop])

        return LineSchedule(line=line, brigades=brigades)

    # TODO: maybe get the full list of stops as an argument here to not reload it without need
    def get_full_schedules(self,
                           routes: dict[str, list[StopInfo]],
                           all_stops: dict[str,
                                           dict[str,
                                                StopLocation]]) -> CompleteSchedule:
        full_schedule: dict[str, LineSchedule] = {}

        for line, stop_infos in routes.items():
            full_schedule[line] = self.__create_line_schedule(line, stop_infos, all_stops)
            print('got line ', line)

        return CompleteSchedule(lines=full_schedule)


if __name__ == '__main__':
    access = EnvApiAccessService()
    sched_s = ApiScheduleService(access)
    route_s = ApiRouteService(access)
    stop_s = ApiStopLocationService(access)

    print('start')

    desired_lines = ['128']
    routes = route_s.get_routes()

    routes = {k: routes[k] for k in routes.keys() if k in desired_lines}

    print('got routes, len: ', len(routes))
    stop_locs = stop_s.get_stop_locations()
    print('got stop locs')

    repo = JSONScheduleRepository()
    schedule = sched_s.get_full_schedules(routes, stop_locs)

    repo.save_schedule(schedule)
