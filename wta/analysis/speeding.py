from datetime import datetime
from typing import Any

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from wta.storage.location_repo import JSONFileLocationRepository
from wta.storage.models import BusHistory, SaveBusData


class SpeedAnnotationService:
    LON_CONV = 111320
    LAT_CONV = 110574

    @classmethod
    def __calc_speed(cls, df: pd.DataFrame) -> Any:
        lon_dist = df['Lon']*cls.LON_CONV
        lat_dist = df['Lat']*cls.LAT_CONV

        meter_dist = np.sqrt(lon_dist**2 + lat_dist**2)

        return (meter_dist / 1000) / (df['Timestamp'] / 3600)


    def get_bus_speeds(self, bhistory: BusHistory) -> pd.DataFrame:
        locations = list(bhistory.times.values())

        loc_df = pd.DataFrame([tuple(bl.model_dump().values(
        )) for bl in locations], columns=list(locations[0].model_fields.keys()) + list(locations[0].model_computed_fields.keys())).drop_duplicates().sort_values(by='Timestamp')
    

        combined = loc_df[['Timestamp', 'Lon', 'Lat']].rolling(2).apply(
            lambda x: np.diff(x))
        combined = combined.assign(speed=SpeedAnnotationService.__calc_speed).sort_values(by='speed')

        full_combined = pd.concat([loc_df, combined['speed']], axis=1)

        # print(full_combined)
    
        # print(full_combined['speed'].mean())
        
        return full_combined

    def get_combined_bus_speeds(self, all_buses: SaveBusData) -> pd.DataFrame:
        buffer = [self.get_bus_speeds(bus) for bus in all_buses.bus_dict.values()]

        return pd.concat(buffer)
    

if __name__ == '__main__':
    plt.scatter(x=[1,2], y=[3,4])
    plt.show()
    locs_repo = JSONFileLocationRepository()
    all_buses = locs_repo.get_locations("./out/locs.json")
    # .bus_dict['1000']

    # SpeedAnnotationService().get_bus_speeds(example)

    df = SpeedAnnotationService().get_combined_bus_speeds(all_buses)
    speeding = df[df.speed > 50.0]

    bounds = (df.Lon.min(), df.Lon.max(), df.Lat.min(), df.Lat.max())




    # print(speeding)
