from pydantic import BaseModel, Extra
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    # mcserver_admin: list
    mcserver: str
    mcserver_apikey: str
