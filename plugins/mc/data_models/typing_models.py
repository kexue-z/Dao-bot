from pydantic import BaseModel


class ServerInfo(BaseModel):
    name: str
    instance_uuid: str
    remote_uuid: str
    status: int
    ip: str
