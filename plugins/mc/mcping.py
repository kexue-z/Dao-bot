# from PIL import Image
# from io import BytesIO
from .statusping import StatusPing
# import base64
import dns.resolver
import json
import re

# from graia.application.message.elements.internal import Image_LocalFile, Plain


def mcping(say):
    # 获取 ping 信息
    host = say.split(":")[0]
    try:
        port = say.split(":")[1]
        get_status = StatusPing(host=host, port=int(port)).get_status()
    except:
        try:
            srv_records = dns.resolver.query("_minecraft._tcp." + host, "SRV")
            srvInfo = {}
            for srv in srv_records:
                srvInfo["host"] = str(srv.target).rstrip(".")
                srvInfo["port"] = srv.port
            get_status = StatusPing(
                host=srvInfo["host"], port=int(srvInfo["port"])
            ).get_status()
        except:
            get_status = StatusPing(host=host).get_status()

    get_status = json.dumps(get_status)
    get_status = re.sub(r"\\u00a7.", "", get_status)
    get_status = json.loads(get_status)
    # print(get_status)

    # 服务器信息解析
    favicon_path = f"mcstatus_temp.jpg"
    msg_send = []

    # 判断是否报错
    if get_status == "error":
        msg_send = f"服务器信息获取失败"
        return msg_send

    # 图标
    # if "favicon" in get_status:
    #     favicon = get_status["favicon"][22:-1] + "="
    #     byte_data = base64.b64decode(favicon)
    #     image_data = BytesIO(byte_data)
    #     img = Image.open(image_data).convert('RGB')
    #     img.save(favicon_path, quality=90)
    #     msg_send.append("[图标]")
    #     msg_send.append(favicon_path)
    #     print("图标已生成")

    # 延迟
    msg_send.append(f"延迟：" + str(get_status["ping"]) + "ms\n")

    # 描述
    if "text" in get_status["description"]:
        sMotd = get_status["description"]["text"]
        msg_send.append(f"Motd：" + sMotd + "\n")
    elif "extra" in get_status["description"]:
        sMotd = ""
        for extra in get_status["description"]["extra"]:
            sMotd = sMotd + extra["text"]
        msg_send.append(f"描述：" + sMotd + "\n")
    elif "translate" in get_status["description"]:
        sMotd = get_status["description"]["translate"]
        msg_send.append(f"描述：" + sMotd + "\n")

    # 服务端版本判断
    if "Requires" in get_status["version"]["name"]:
        sType = "Vanilla"
        sVer = get_status["version"]["name"]
    else:
        if get_status["version"]["name"].find(" ") > 0:
            serType = get_status["version"]["name"].rsplit(" ", 1)
            sType = serType[0]
            sVer = serType[1]
            # print(serType)
            # print(sType)
            # print(sVer)
        else:
            sType = "Vanilla"
            sVer = get_status["version"]["name"]

    sDevVer = str(get_status["version"]["protocol"])
    sPlayer = (
        str(get_status["players"]["online"]) + " / " + str(get_status["players"]["max"])
    )

    msg_send.append(f"游戏版本：" + sVer + "\n")
    msg_send.append(f"协议版本：" + sDevVer + "\n")
    msg_send.append(f"服务端：" + sType + "\n")

    # 玩家数
    msg_send.append(f"玩家数：" + sPlayer)

    # 判断是否存在在线玩家
    if "sample" in get_status["players"] and get_status["players"]["sample"] != []:
        sOnlinePlayer = []
        for player in get_status["players"]["sample"]:
            sOnlinePlayer.append(player["name"])
        msg_send.append(f"\n在线玩家：" + " | ".join(sOnlinePlayer))

    # 如果为原版 Forge
    if "modinfo" in get_status:
        if "FML" in get_status["modinfo"]["type"]:
            sModApi = "Forge"
            msg_send.append(f"\n模组Api：" + sModApi)

    # Mod 列表
    if "modinfo" in get_status:
        sModsNum = str(len(get_status["modinfo"]["modList"]))
        # sMods = []
        # mod_num = 0
        # for mod in get_status["modinfo"]["modList"]:
        #     sMods.append(mod["modid"] + "@" + mod["version"])
        #     mod_num = mod_num + 1
        #     if mod_num == 20:
        #         sMods.append("......（仅显示前 20 个 mod）")
        #         break
        msg_send.append(f"\nMod数：" + sModsNum + " +")
    elif "forgeData" in get_status:
        sModsNum = str(len(get_status["forgeData"]["mods"]))
        # sMods = []
        # mod_num = 0
        # for mod in get_status["forgeData"]["mods"]:
        #     sMods.append(mod["modId"] + "@" + mod["modmarker"])
        #     mod_num = mod_num + 1
        #     if mod_num == 20:
        #         sMods.append("......（仅显示前 20 个 mod）")
        #         break
        msg_send.append(f"\nMod数：" + sModsNum + " +")

    return msg_send
