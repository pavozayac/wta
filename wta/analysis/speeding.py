from wta.storage.location_repo import JSONFileLocationRepository
from datetime import datetime

import pandas as pd
import numpy as np

from wta.storage.models import BusHistory


# def pd_timedelta(two: datetime):
#     print(two)
#     return pd.Timedelta(pd.to_datetime(two[1]) - pd.to_datetime(two[0])).seconds


def analyse_speeding(bhistory: BusHistory):
    # locs_repo = JSONFileLocationRepository('./out/locs.json')

    locations = list(bhistory.times.values())

    loc_df = pd.DataFrame([tuple(bl.model_dump().values(
    )) for bl in locations], columns=list(locations[0].model_fields.keys()) + list(locations[0].model_computed_fields.keys()))

    time_diff = loc_df['Timestamp'].rolling(2).apply(
        lambda x: np.diff(x))
    # .apply(pd_timedelta)
    lon_diff = loc_df['Lon'].rolling(2).apply(
        lambda x: np.diff(x))
    lat_diff = loc_df['Lat'].rolling(2).apply(
        lambda x: np.diff(x))

    combined = pd.concat([lat_diff, lon_diff, time_diff], axis=1)

    combined = combined.assign(speed=lambda df: np.sqrt(
        df['Lon']**2 + df['Lat']**2) / df['Timestamp'])

    print(combined)

    # print(loc_df)
    # print(loc_df.drop_duplicates())

    # print(loc_df[['Time', 'VehicleNumber']].sort_values('Time'))


if __name__ == '__main__':
    locs_repo = JSONFileLocationRepository('./out/locs.json')
    example = locs_repo.get_locations().bus_dict['1000']

    analyse_speeding(example)
