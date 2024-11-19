from __future__ import annotations

from typing import List

from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    nickname: str


class Datum(BaseModel, extra=Extra.ignore):
    instanceUuid: str
    status: int
    config: Config


class Data(BaseModel, extra=Extra.ignore):
    page: int
    pageSize: int
    maxPage: int
    data: List[Datum]


class RemoteServicesApi(BaseModel, extra=Extra.ignore):
    status: int
    data: Data
    time: int
