from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    repeat_count: int = 2
