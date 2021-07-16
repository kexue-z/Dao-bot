from nonebot.adapters.cqhttp.bot import Bot, Event
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.plugin import require

# TOPIC = "nonebot"

export = require("nonebot_plugin_mqtt")
export.mqtt_client.on_message = on_message
@export.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await bot.send(event, message="555", )

# export.mqtt_client.publish("nonebot","msg")
# export.mqtt_client.subscribe(TOPIC, qos=1)



print(export)