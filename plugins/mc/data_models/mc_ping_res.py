from typing import List

from pydantic import BaseModel


class MCPing(BaseModel):
    name: str
    ip: str | None
    version: str
    player_online: int
    max_online: int
    player_list: List[str]
    latency: int
    motd: str
    mcsm_status: int
