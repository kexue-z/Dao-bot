from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    # mcserver_admin: list
    mcserver: str
    mcserver_apikey: str
