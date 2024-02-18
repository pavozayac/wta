
from wta.analysis.speeds import SpeedAnnotationService
from wta.storage.models import SaveBusData


class SpeedingLocationService:

    def __init__(self, speed_service: SpeedAnnotationService) -> None:
        self.speed_service = speed_service

    def get_annotated_locations(self, save_data: SaveBusData, radius=50):
        speed_annonated = self.speed_service.get_combined_bus_speeds(save_data)
