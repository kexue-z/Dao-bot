from typing import List
from datetime import datetime

from nonebot.log import logger
from models.mc import MCServers, KookMsg

from .utils import make_card
from .typing_models import ServerInfo
from ..mcsm import call_server, search_remote_services


async def get_server_status(expeire_time: datetime):
    remote_uuids: List[str] = (
        await MCServers.all().distinct().values_list("remote_uuid", flat=True)
    )  # type: ignore
    logger.trace(remote_uuids)

    all_services: List[ServerInfo] = []

    usable: List[str] = (
        await MCServers.all().distinct().values_list("instance_uuid", flat=True)
    )  # type: ignore

    logger.trace(usable)

    # 逐个获取守护进程内的实例
    for remote in remote_uuids:
        services = await search_remote_services(remote)

        for service in services.data.data:
            if service.instanceUuid in usable:
                all_services.append(
                    ServerInfo(
                        name=service.config.nickname,
                        instance_uuid=service.instanceUuid,
                        remote_uuid=remote,
                        status=service.status,
                    )
                )

    # return make_card(all_services)
    if all_services:
        return make_card(all_services, expeire_time)
    return None
