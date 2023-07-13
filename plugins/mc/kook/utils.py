from datetime import datetime
from typing import Any, Dict, List

from khl_card.card import Card
from khl_card.accessory import Button
from khl_card.accessory import Kmarkdown as KMD
from khl_card.modules import Context, ActionGroup
from khl_card.types import KmarkdownColors as KMDC
from khl_card.accessory import PlainText, ThemeTypes
from khl_card.builder import CardBuilder, CardMessageBuilder

from ..data_models.typing_models import ServerInfo


def make_server_card(card: CardBuilder, server: ServerInfo):
    status_dict = {
        -1: KMD.color("状态未知", color=KMDC.SECONDARY),
        0: KMD.color("已停止", color=KMDC.DANGER),
        1: KMD.color("正在停止", color=KMDC.WARNING),
        2: KMD.color("正在启动", color=KMDC.PRIMARY),
        3: KMD.color("正在运行", color=KMDC.SUCCESS),
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
                    value=f"{server.instance_uuid}:open",
                    click="return-val",
                ),
                Button(
                    PlainText(":x: 关闭", emoji=True),
                    theme=ThemeTypes.WARNING,
                    value=f"{server.instance_uuid}:stop",
                    click="return-val",
                ),
                Button(
                    PlainText(":recycle: 重启", emoji=True),
                    theme=ThemeTypes.INFO,
                    value=f"{server.instance_uuid}:restart",
                    click="return-val",
                ),
            )
        )
        .build()
    )


def make_card(
    server_list: List[ServerInfo], expeire_time: datetime
) -> List[Dict[Any, Any]]:
    time_format = r"%Y-%m-%d %H:%M:%S"
    cb = (
        CardBuilder()
        .header(PlainText(":rocket:MCSM 服务器管理", emoji=True))
        .divider()
        .second_countdown(
            end_time=expeire_time.strftime(time_format),
            start_time=datetime.now().strftime(time_format),
        )
    )

    servers_card = Card()

    for s in server_list:
        servers_card = make_server_card(cb, s)

    return CardMessageBuilder().card(servers_card).build().build()


def make_done_card(server_name: str, funcs: str):
    msg = KMD(f"~~该卡片已被使用~~\n **{server_name}:**已发送指令 `{funcs}`")

    cb = (
        CardBuilder()
        .header(PlainText(":rocket:MCSM 服务器管理", emoji=True))
        .divider()
        .context(Context(msg))
    ).build()

    return CardMessageBuilder().card(cb).build().build()


def make_outdate_card():
    msg = KMD.strikethrough("该卡片已过期")

    cb = (
        CardBuilder()
        .header(PlainText(":rocket:MCSM 服务器管理", emoji=True))
        .divider()
        .context(Context(msg))
    ).build()

    return CardMessageBuilder().card(cb).build().build()


def make_error_card(err: str):
    msg = KMD(err)

    cb = (
        (
            CardBuilder()
            .header(PlainText(":rocket:MCSM 服务器管理", emoji=True))
            .divider()
            .context(Context(msg))
        )
        .build()
        .set_theme(ThemeTypes.WARNING)
    )

    return CardMessageBuilder().card(cb).build().build()


from ..data_models.mc_ping_res import MCPing

STATUS_DICT = {
    -1: "状态未知",
    0: "已停止",
    1: "正在停止",
    2: "正在启动",
    3: "正在运行",
}
STATUS_THEME_DICT = {
    -1: ThemeTypes.SECONDARY,
    0: ThemeTypes.DANGER,
    1: ThemeTypes.WARNING,
    2: ThemeTypes.INFO,
    3: ThemeTypes.SUCCESS,
}


def ping_card(p: MCPing) -> Card:
    return (
        CardBuilder()
        .header(f"{p.name} {p.ip}")
        .divider()
        .context(
            Context(
                KMD(f"延迟: **{p.latency}ms**\n"),
                KMD(f"MOTD: **{p.motd}**\n"),
                KMD(f"游戏版本: **{p.version}**"),
                KMD(f"玩家数: **{p.player_online}/{p.max_online}**"),
                KMD(f"在线玩家: **{','.join([_p for _p in p.player_list])}**"),
            )
        )
        .build()
        .set_theme(STATUS_THEME_DICT[p.mcsm_status])
    )


def make_ping_card(mcping: List[MCPing]):
    cmb = CardMessageBuilder()
    cmb = cmb.card(
        CardBuilder().header(PlainText(":rocket:MC 服务器详情", emoji=True)).build()
    )

    for s in mcping:
        cmb = cmb.card(ping_card(s))

    return cmb.build().build()
