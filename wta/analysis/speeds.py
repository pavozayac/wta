from datetime import datetime
from typing import Any

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

from wta.analysis.clusters import ClusterAnalysisService
from wta.storage.location_repo import JSONLocationRepository
from wta.storage.models import BusHistory, SaveBusData
from wta.storage.processing_repo import CsvRepo, DataFrameRepo


class SpeedAnnotationService:
    LON_CONV = 111320
    LAT_CONV = 110574

    def __init__(self, repo: DataFrameRepo = CsvRepo()) -> None:
        self.repo = repo

    @classmethod
    def __calc_speed(cls, df: pd.DataFrame) -> Any:
        lon_dist = df['Lon'] * cls.LON_CONV
        lat_dist = df['Lat'] * cls.LAT_CONV

        meter_dist = np.sqrt(lon_dist**2 + lat_dist**2)

        return (meter_dist / 1000.0) / (df['Timestamp'] / 3600)

    @staticmethod
    def get_bus_speeds(bhistory: BusHistory) -> pd.DataFrame:
        locations = list(bhistory.times.values())

        loc_df = pd.DataFrame(
            [
                tuple(
                    bl.model_dump().values()) for bl in locations],
            columns=list(
                locations[0].model_fields.keys()) +
            list(
                locations[0].model_computed_fields.keys())).drop_duplicates().sort_values(
            by='Timestamp')

        combined = loc_df[['Timestamp', 'Lon', 'Lat']].rolling(2).apply(
            lambda x: np.diff(x))
        combined = combined.assign(
            speed=SpeedAnnotationService.__calc_speed).sort_values(
            by='speed')

        full_combined = pd.concat([loc_df, combined['speed']], axis=1)

        return full_combined

    def get_combined_bus_speeds(self, all_buses: SaveBusData) -> pd.DataFrame:
        buffer = [self.get_bus_speeds(bus) for bus in all_buses.bus_dict.values()]
        result = pd.concat(buffer)

        # print(result['speed'].max())

        # self.repo.save_csv(result)

        return result


if __name__ == '__main__':
    locs_repo = JSONLocationRepository()
    all_buses = locs_repo.get_locations()
    # .bus_dict['1000']

    # SpeedAnnotationService().get_bus_speeds(example)

    repo = CsvRepo()

    df = None

    try:
        df = repo.load_csv()
    except FileNotFoundError:
        df = SpeedAnnotationService().get_combined_bus_speeds(all_buses)

    speeding = df[(df.speed > 60.0) & (df.speed < 150.0)]

    overspeeding = df[df.speed >= 150.0]

    print(len(overspeeding.index) / len(df.index))

    fig = px.scatter_mapbox(
        speeding,
        lat='Lat',
        lon='Lon',
        hover_data=['speed'],
        color='speed',
    )

    fig.update_layout(mapbox_style='open-street-map')

    fig.show()

    clusters, noise = ClusterAnalysisService.get_clusters(speeding, 0.001)

    fig2 = px.scatter_mapbox(
        clusters,
        lat='Lat',
        lon='Lon',
        color_discrete_sequence=[px.colors.label_rgb((255, 0, 0))]
    )

    fig2.update_layout(mapbox_style='open-street-map')

    fig2.show()
