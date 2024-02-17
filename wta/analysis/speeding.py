from datetime import datetime
from typing import Any

import pandas as pd
import numpy as np

from wta.storage.location_repo import JSONFileLocationRepository
from wta.storage.models import BusHistory


def calc_speed(df: pd.DataFrame) -> Any:
    lon_dist = df['Lon']*111320
    lat_dist = df['Lat']*110574

    meter_dist = np.sqrt(lon_dist**2 + lat_dist**2)

    return (meter_dist / 1000) / (df['Timestamp'] / 3600)


def analyse_speeding(bhistory: BusHistory):
    locations = list(bhistory.times.values())

    loc_df = pd.DataFrame([tuple(bl.model_dump().values(
    )) for bl in locations], columns=list(locations[0].model_fields.keys()) + list(locations[0].model_computed_fields.keys())).drop_duplicates()
    

    combined = loc_df[['Timestamp', 'Lon', 'Lat']].rolling(2).apply(
        lambda x: np.diff(x))

    combined = combined.assign(speed=calc_speed).sort_values(by='speed')

    print(combined)
    print(combined['speed'].mean())
    
    print(loc_df['Lat'].min(), loc_df['Lat'].max(), loc_df['Lon'].min(), loc_df['Lon'].max())

if __name__ == '__main__':
    locs_repo = JSONFileLocationRepository()
    example = locs_repo.get_locations("./out/locs.json").bus_dict['1000']

    analyse_speeding(example)
