from abc import ABC, abstractmethod
import os


class ApiAccessService(ABC):

    @abstractmethod
    def api_key(self) -> str:
        pass


class EnvApiAccessService(ApiAccessService):

    def __init__(self, var_name='WTA_API_KEY') -> None:
        self.ENV_VAR_NAME = var_name

    def api_key(self) -> str:
        if self.ENV_VAR_NAME not in os.environ:
            raise KeyError(
                f'Environment variable {self.ENV_VAR_NAME} was not found.')

        return os.environ[self.ENV_VAR_NAME]
