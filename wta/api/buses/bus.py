from .models import BusLocation


class Bus:

    def __init__(self, location_history: list[BusLocation]) -> None:
        self.location_history = location_history

    def history(self) -> list[BusLocation]:
        return self.location_history
