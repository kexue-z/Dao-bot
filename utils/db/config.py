from typing import Optional

from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str
