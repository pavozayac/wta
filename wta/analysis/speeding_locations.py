import pandas as pd

from wta.analysis.speeds import SpeedAnnotationService
from wta.storage.models import SaveBusData
from wta.storage.processing_repo import CsvRepo


class SpeedingLocationService:

    def __init__(self, speed_service: SpeedAnnotationService,
                 ) -> None:
        # self.repo = repo
        self.speed_service = speed_service

    def get_annotated_locations(self, save_data: SaveBusData) -> pd.DataFrame:
        df = None

        # try:
        #     df = self.repo.load_csv()
        # except FileNotFoundError:
        df = self.speed_service.get_combined_bus_speeds(save_data)
        # self.repo.save_csv(df)

        speeding = df[(df.speed > 60.0) & (df.speed < 150.0)]

        return speeding
