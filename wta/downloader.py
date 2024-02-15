import datetime
import os
from wta.api.buses.bus_location_service import ApiBusLocationService
from wta.api.access_service import EnvApiAccessService

from wta.api.buses.models import BusLocationList
from wta.exceptions.undef_server_behaviour import UndefinedServerBehaviourError
from wta.storage.location_repo import JSONFileLocationRepository

file_name = './out/locs.json'

if os.path.exists(file_name):
    os.remove(file_name)

access_service = EnvApiAccessService()
locs_service = ApiBusLocationService()
locs_repo = JSONFileLocationRepository(file_name)


start = datetime.datetime.now()
end = start + datetime.timedelta(minutes=15)

while datetime.datetime.now() < end:
    try:
        locs = locs_service.get_bus_locations(access_service)
        locs_repo.save_locations(BusLocationList(locations=locs))

    except UndefinedServerBehaviourError:
        pass
