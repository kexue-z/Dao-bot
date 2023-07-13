from json import dumps
from typing import List
from datetime import datetime, timedelta

from dateutil import tz
from nonebot.log import logger
from models.mc import KookMsg, MCServers
from nonebot.adapters.kaiheila import Bot, Event
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.kaiheila.event import CartBtnClickNoticeEvent

from ..data_models.typing_models import ServerInfo
from .utils import make_card, make_done_card, make_error_card, make_outdate_card
from ..mcsm import MCSMAPIError, HTTPStatusError, call_server, search_remote_services


async def get_server_status():
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

    return all_services


async def make_control_card(expeire_time: datetime) -> List:
    # res = await get_server_status()

    res = [
        ServerInfo(
            name="test", instance_uuid="instance", remote_uuid="remote", status=1
        )
    ]

    return make_card(res, expeire_time)


async def button_event(bot: Bot, event: Event):
    if isinstance(event, CartBtnClickNoticeEvent):
        data = event.extra
        if data.body:
            value: str = data.body.get("value")  # type: ignore
            msg_id: str = data.body.get("msg_id")  # type: ignore
            user_id: str = data.body.get("user_id")  # type: ignore

            instance_uuid = value.split(":", 1)[0]
            funcs = value.split(":", 1)[1]

            logger.debug(
                f"Got value: {value} msg_id: {msg_id} user_id: {user_id} instance_id: {instance_uuid} funcs: {funcs}"
            )

            record = await KookMsg.get(msg_id=msg_id)

            if not (
                user_id == user_id
                and record.expeire_time.astimezone(tz.tzlocal())
                >= datetime.now(tz=tz.tzlocal())
            ):
                return False

            server = await MCServers.get(instance_uuid=instance_uuid)

            # 获取服务器名称
            server_name = ""
            server_list = await get_server_status()
            for server in server_list:
                if server.instance_uuid == instance_uuid:
                    server_name = server.name

            # 调用API
            try:
                await call_server(
                    type=funcs,
                    instance_uuid=instance_uuid,
                    remote_uuid=server.remote_uuid,
                )

                # 操作成功
                await bot.message_update(
                    msg_id=msg_id,
                    content=dumps(
                        make_done_card(server_name=server_name, funcs=funcs),
                        ensure_ascii=False,
                    ),
                )
                return True

            except MCSMAPIError as e:
                msg = f":collision: MCSM API错误: (ins){e}(ins)"

                await bot.message_update(
                    msg_id=msg_id,
                    content=dumps(
                        make_error_card(msg),
                        ensure_ascii=False,
                    ),
                )

            except HTTPStatusError as e:
                msg = f":collision: HTTP错误: (ins){e}(ins)"

                await bot.message_update(
                    msg_id=msg_id,
                    content=dumps(
                        make_error_card(msg),
                        ensure_ascii=False,
                    ),
                )

            finally:
                return False


def set_outdate_card_scheduler(bot: Bot, msg_id: str, time: datetime):
    async def set_card_job(bot: Bot, msg_id: str):
        await bot.message_update(
            msg_id=msg_id,
            content=dumps(
                make_outdate_card(),
                ensure_ascii=False,
            ),
        )

    action_time = time + timedelta(seconds=30)

    scheduler.add_job(
        set_card_job, trigger="date", run_date=action_time, args=[bot, msg_id]
    )
