import pandas as pd
from wta.api.schedules.models import CompleteSchedule
from wta.storage.full_schedule_repo import JSONScheduleRepository
from wta.storage.location_repo import JSONLocationRepository
from wta.storage.models import SaveBusData
from wta.storage.processing_repo import CsvRepo


class LatenessService:
    def analyze_lateness(self, schedule: CompleteSchedule, locations: SaveBusData):
        lines = schedule.lines.keys()

        # loc_df = CsvRepo().load_csv()
        sched_df = pd.DataFrame.from_dict(schedule.model_dump())


if __name__ == '__main__':
    LatenessService().analyze_lateness(
        JSONScheduleRepository().get_schedule(),
        JSONLocationRepository().get_locations('./out/locs.json'))
