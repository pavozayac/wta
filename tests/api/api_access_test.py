import os

from wta.api.access_service import EnvApiAccessService

def should_get_key_from_env():
    test_key = 'example'
    os.environ['WTA_API_KEY'] = test_key

    sut = EnvApiAccessService()

    assert sut.api_key() == test_key
