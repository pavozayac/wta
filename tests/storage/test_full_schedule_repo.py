# Write a test similar to test_location_repo.py, but for the JSONScheduleRepository class.
from wta.storage.full_schedule_repo import JSONScheduleRepository


def test_should_return_empty_on_not_found():
    weird_file = './abcedefghijklmnop.bin'
    loc_repo = JSONScheduleRepository(weird_file)

    result = loc_repo.get_schedule()

    assert len(result.lines) == 0
    