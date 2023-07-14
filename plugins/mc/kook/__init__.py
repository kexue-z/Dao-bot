from datetime import datetime, timedelta

from dateutil import tz
from nonebot.rule import Rule
from nonebot.log import logger
from nonebot.typing import T_State
from models.mc import KookMsg, UserFrom, MCTrustIDs
from nonebot.adapters.kaiheila import Bot, Event, Message
from nonebot.adapters.kaiheila import MessageSegment as KMS
from nonebot.adapters.kaiheila.api import MessageCreateReturn
from nonebot import on_notice, get_driver, on_command, on_message
from nonebot.adapters.kaiheila.event import CartBtnClickNoticeEvent

from .data_source import button_event, make_control_card, set_outdate_card_scheduler

superusers = get_driver().config.superusers


async def is_whitelist(event: Event):
    if int(event.user_id) not in await MCTrustIDs.get_all_enabled_ids(
        user_from=UserFrom.Kook
    ):
        return True

    if event.user_id in superusers:
        return True

    return False


def is_kook(bot: Bot):
    if isinstance(bot, Bot):
        return True
    return False


def kook_command_start(event: Event):
    msg_list = event.get_plaintext().split(maxsplit=1)
    if "mcsmadd" in msg_list[0]:
        return True
    return False


def is_button_event(event: Event):
    if isinstance(event, CartBtnClickNoticeEvent):
        return True
    return False


async def is_in_button_msg(state: T_State, event: Event):
    data = event.extra
    if data.body:
        value: str = data.body.get("value")  # type: ignore
        msg_id: str = data.body.get("msg_id")  # type: ignore
        user_id: str = data.body.get("user_id")  # type: ignore

        instance_uuid = value.split(":", 1)[0]
        funcs = value.split(":", 1)[1]

        state["msg_id"] = msg_id
        state["funcs"] = funcs
        state["instance_uuid"] = instance_uuid

        logger.debug(
            f"Got value: {value} msg_id: {msg_id} user_id: {user_id} instance_id: {instance_uuid} funcs: {funcs}"
        )

        record = await KookMsg.get(msg_id=msg_id)

        if int(user_id) == record.user_id and record.expeire_time.astimezone(
            tz.tzlocal()
        ) >= datetime.now(tz=tz.tzlocal()):
            return True

    return False


kmcsm_add = on_message(
    rule=Rule(
        is_kook,
        kook_command_start,
        is_whitelist,
    ),
    block=True,
)
"""KOOK: 添加控制服务器的权限"""


@kmcsm_add.handle()
async def _(event: Event):
    user_id_list = event.extra.mention if event.extra.mention else []
    ok = []
    for user_id in user_id_list:
        ok.append(await MCTrustIDs.add_id(int(user_id), user_from=UserFrom.Kook))

    if ok:
        await kmcsm_add.finish("已添加")


kmcsm = on_command(
    "mcsm",
    priority=4,
    block=True,
    rule=Rule(
        is_kook,
        is_whitelist,
    ),
)
"""KOOK: 开关服务器"""


@kmcsm.handle()
async def _(bot: Bot, event: Event):
    expeire_time = datetime.now() + timedelta(minutes=1)

    if card := await make_control_card(expeire_time=expeire_time):
        msg: MessageCreateReturn = await kmcsm.send(Message(KMS.Card(card)))
        if msg.msg_id:
            record = await KookMsg.create(
                msg_id=msg.msg_id,
                user_id=int(event.user_id),
                expeire_time=expeire_time,
            )
            await record.save()

            set_outdate_card_scheduler(bot, msg.msg_id, expeire_time)

    else:
        msg = await kmcsm.send("无可用服务器")

    await kmcsm.finish()


kmcsm_button = on_notice(
    rule=Rule(
        is_button_event,
        is_in_button_msg,
    )
)
"""KOOK: 按钮事件"""


@kmcsm_button.handle()
async def _(bot: Bot, state: T_State):
    await button_event(bot, state)
    await kmcsm_button.finish()
