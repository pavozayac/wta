import datetime
import os
from time import sleep
import base64
import re

from wta.api.locations.bus_location_service import ApiBusLocationService, BusLocationService
from wta.api.generic.access_service import ApiAccessService, EnvApiAccessService

from wta.api.locations.models import BusLocationList
from wta.exceptions.undef_server_behaviour import UndefinedServerBehaviourError
from wta.storage.location_repo import JSONFileLocationRepository, LocationRepository


class LocationDownloaderService:

    def __init__(
            self,
            access_service: ApiAccessService,
            location_service: BusLocationService,
            location_repo: LocationRepository,
            file_name=None) -> None:
        self.access_service = access_service
        self.location_service = location_service
        self.location_repo = location_repo

        if file_name is not None:
            self.file_name = file_name
        else:
            slug_fname = re.sub(r"[\W]", "_", str(datetime.datetime.now()))
            print(slug_fname)
            self.file_name = f'./out/{slug_fname}.json'

    def download(self, interval_secs=10, total_mins=60):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

        start = datetime.datetime.now()
        end = start + datetime.timedelta(minutes=total_mins)

        while datetime.datetime.now() < end:
            try:
                locs = self.location_service.get_bus_locations(self.access_service)
                self.location_repo.save_locations(BusLocationList(locations=locs), self.file_name)

                sleep(interval_secs)

            except UndefinedServerBehaviourError:
                pass


if __name__ == '__main__':
    downloader = LocationDownloaderService(
        EnvApiAccessService(),
        ApiBusLocationService(),
        JSONFileLocationRepository())

    downloader.download(10, 1)
