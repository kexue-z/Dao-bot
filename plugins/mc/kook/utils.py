from typing import Any, Dict, List

from khl_card.card import Card
from khl_card.accessory import Button
from khl_card.accessory import Kmarkdown as KMD
from khl_card.modules import Context, ActionGroup
from khl_card.types import KmarkdownColors as KMDC
from khl_card.accessory import PlainText, ThemeTypes
from khl_card.builder import CardBuilder, CardMessageBuilder

from .typing_models import ServerInfo


def make_server_card(card: CardBuilder, server: ServerInfo):
    status_dict = {
        -1: KMD.color("状态未知", color=KMDC.INFO),
        0: KMD.color("已停止", color=KMDC.WARNING),
        2: KMD.color("正在启动", color=KMDC.SECONDARY),
        3: KMD.color("正在运行", color=KMDC.PRIMARY),
    }

    msg = KMD("状态: ") + status_dict[server.status] + KMD("\n")

    return (
        card.divider()
        .header(server.name)
        .context(Context(msg))
        .action_group(
            ActionGroup(
                Button(
                    PlainText(":heavy_check_mark: 开启", emoji=True),
                    theme=ThemeTypes.PRIMARY,
                    value=f"{server.instance_uuid}:ON",
                    click="return-val",
                ),
                Button(
                    PlainText(":x: 关闭", emoji=True),
                    theme=ThemeTypes.WARNING,
                    value=f"{server.instance_uuid}:OFF",
                    click="return-val",
                ),
                Button(
                    PlainText(":recycle: 重启", emoji=True),
                    theme=ThemeTypes.INFO,
                    value=f"{server.instance_uuid}:RESTART",
                    click="return-val",
                ),
            )
        )
        .build()
    )


def make_card(server_list: List[ServerInfo]) -> List[Dict[Any, Any]]:
    cb = CardBuilder().header(PlainText(":rocket:MCSM 服务器管理", emoji=True))

    servers_card = Card()

    for s in server_list:
        servers_card = make_server_card(cb, s)

    return CardMessageBuilder().card(servers_card).build().build()
