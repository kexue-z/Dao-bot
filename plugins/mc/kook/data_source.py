from typing import List

from nonebot.log import logger
from models.mc import MCServers

from .utils import make_card
from .typing_models import ServerInfo
from ..mcsm import search_remote_services


async def get_server_status():
    remote_uuids: List[str] = await MCServers.all().values_list("remote_uuid", flat=True)  # type: ignore
    logger.debug(remote_uuids)

    all_services: List[ServerInfo] = []

    # 逐个获取守护进程内的实例
    for remote in remote_uuids:
        # for remote in ["remote1", "remote2", "remote3", "remote4"]:
        services = await search_remote_services(remote)
        # TODO
        services = [
            ServerInfo(
                name="name",
                instance_uuid="instance",
                remote_uuid=remote,
                started=1,
                status=3,
            )
        ]

        # 添加到所有列表中
        all_services += services
        logger.debug(remote)

    # 仅保留在可用列表中的示例

    usable: List[str] = await MCServers.all().values_list("instance_uuid", flat=True)  # type: ignore

    _all_services: List[ServerInfo] = []

    for service in all_services:
        if service.instance_uuid in usable:
            _all_services.append(service)

    # return make_card(all_services)
    if _all_services:
        return make_card(_all_services)
    return None
