from wta.api.buses.bus_location_service import ApiBusLocationService
from wta.api.access_service import EnvApiAccessService

access_service = EnvApiAccessService()
locs_service = ApiBusLocationService()


for b in locs_service.get_bus_locations(access_service):
    print(b)
