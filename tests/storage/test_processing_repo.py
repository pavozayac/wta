import pytest
from wta.storage.processing_repo import CsvRepo

def test_should_return_empty_on_not_found():
    weird_file = './abcedefghijklmnop.bin'
    loc_repo = CsvRepo(weird_file)

    assert pytest.raises(FileNotFoundError, loc_repo.load_csv)
