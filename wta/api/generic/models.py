from pydantic import BaseModel

class GenericKeyValue(BaseModel):
    value: str
    key: str


class GenericKVList(BaseModel):
    values: list[GenericKeyValue]


class GenericKVResponse(BaseModel):
    result: list[GenericKVList]