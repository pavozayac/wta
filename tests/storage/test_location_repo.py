from wta.storage.location_repo import JSONLocationRepository


def test_should_return_empty_on_not_found():
    weird_file = './abcedefghijklmnop.bin'
    loc_repo = JSONLocationRepository(weird_file)

    result = loc_repo.get_locations().bus_dict

    assert len(result) == 0
