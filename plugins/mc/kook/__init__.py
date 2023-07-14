from datetime import datetime, timedelta

from nonebot.rule import Rule
from nonebot.log import logger
from models.mc import KookMsg, UserFrom, MCTrustIDs
from nonebot import on_notice, on_command, on_message
from nonebot.adapters.kaiheila import Bot, Event, Message
from nonebot.adapters.kaiheila import MessageSegment as KMS
from nonebot.adapters.kaiheila.api import MessageCreateReturn

from .data_source import button_event, make_control_card, set_outdate_card_scheduler


async def is_kook(bot: Bot):
    if isinstance(bot, Bot):
        return True
    return False


async def kook_command_start(event: Event):
    msg_list = event.get_plaintext().split(maxsplit=1)
    if "mcsmadd" in msg_list[0]:
        return True
    return False


kmcsm_add = on_message(rule=Rule(is_kook, kook_command_start), block=True)
"""KOOK: 添加控制服务器的权限"""


@kmcsm_add.handle()
async def _(event: Event):
    msg = event.get_plaintext()
    logger.debug(msg)
    user_id_list = event.extra.mention if event.extra.mention else []
    for user_id in user_id_list:
        logger.debug(user_id)


kmcsm = on_command("mcsm", priority=1, block=True)
"""KOOK: 开关服务器"""


@kmcsm.handle()
async def _(bot: Bot, event: Event):
    if int(event.user_id) not in await MCTrustIDs.get_all_enabled_ids(
        user_from=UserFrom.Kook
    ):
        await kmcsm.finish("你没有权限使用这个命令")

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

            set_outdate_card_scheduler(bot, msg.msg_id, expeire_time, id=msg.msg_id)

    else:
        msg = await kmcsm.send("无可用服务器")

    await kmcsm.finish()


kmcsm_button = on_notice()
"""KOOK: 按钮事件"""


@kmcsm_button.handle()
async def _(bot: Bot, event: Event):
    await button_event(bot, event)
    await kmcsm_button.finish()
