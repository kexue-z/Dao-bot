from typing import Optional

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    # mcserver_admin: list
    mcserver: str
    mcserver_apikey: str
