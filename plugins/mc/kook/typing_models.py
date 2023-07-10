from pydantic import BaseModel


class ServerInfo(BaseModel):
    name: str
    instance_uuid: str
    remote_uuid: str
    started: int
    status: int
    ip: str | None = None
