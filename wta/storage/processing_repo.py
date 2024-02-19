from abc import ABC, abstractmethod
import os
import pandas as pd


class DataFrameRepo(ABC):

    @abstractmethod
    def save_csv(self, df: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def load_csv(self) -> pd.DataFrame:
        pass


class CsvRepo(DataFrameRepo):

    def __init__(self, file_name: str = './out/processed/speeds.csv') -> None:
        self.file_name = file_name

    def save_csv(self, df: pd.DataFrame) -> None:
        if not os.path.exists(os.path.dirname(self.file_name)):
            os.makedirs(os.path.dirname(self.file_name))

        df.to_csv(self.file_name)

    def load_csv(self) -> pd.DataFrame:
        if not os.path.exists(self.file_name):
            raise FileNotFoundError

        return pd.read_csv(self.file_name)
