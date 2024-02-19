from pydantic import BaseModel


class RouteStop(BaseModel):
    odleglosc: int
    ulica_id: str
    nr_zespolu: str
    typ: str
    nr_przystanku: str


class RouteResponse(BaseModel):
    result: dict[str, dict[str, dict[str, RouteStop]]]
