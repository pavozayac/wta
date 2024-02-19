import os

from wta.api.generic.access_service import EnvApiAccessService


def test_should_get_key_from_env():
    test_key = 'example'
    os.environ['WTA_API_KEY'] = test_key

    sut = EnvApiAccessService()

    assert sut.api_key() == test_key


def test_should_get_url_from_env():
    test_url = 'example_url'
    os.environ['WTA_BASE_URL'] = test_url

    sut = EnvApiAccessService()

    assert sut.base_api_url() == test_url
