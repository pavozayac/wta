from wta.storage.location_repo import JSONFileLocationRepository
from datetime import datetime

import pandas as pd


def pd_timedelta(two: datetime):
    print(two)
    return pd.Timedelta(pd.to_datetime(two[1]) - pd.to_datetime(two[0])).seconds


def analyse_speeding():
    locs_repo = JSONFileLocationRepository('./out/locs.json')

    locations = locs_repo.get_locations().locations

    loc_df = pd.DataFrame([tuple(bl.model_dump().values(
    )) for bl in locations], columns=locations[0].model_fields.keys())

    tds = loc_df['Time'].rolling(2).sum()
    # .apply(pd_timedelta)

    print(tds)

    print(loc_df)
    print(loc_df.drop_duplicates())

    print(loc_df[['Time', 'VehicleNumber']].sort_values('Time'))


if __name__ == '__main__':
    analyse_speeding()
