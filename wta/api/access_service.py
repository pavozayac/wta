from abc import ABC, abstractmethod
import os


class ApiAccessService(ABC):

    @abstractmethod
    def api_key(self) -> str:
        pass

    def base_api_url(self) -> str:
        pass


class EnvApiAccessService(ApiAccessService):

    def __init__(self, key_name='WTA_API_KEY', base_url_name='WTA_BASE_URL') -> None:
        self.KEY_NAME = key_name
        self.BASE_URL_NAME = base_url_name

    def api_key(self) -> str:
        if self.KEY_NAME not in os.environ:
            raise KeyError(
                f'Environment variable {self.KEY_NAME} was not found.')

        return os.environ[self.KEY_NAME]

    def base_api_url(self) -> str:
        if self.BASE_URL_NAME not in os.environ:
            raise KeyError(
                f'Environment variable {self.BASE_URL_NAME} was not found.')

        return os.environ[self.BASE_URL_NAME]
