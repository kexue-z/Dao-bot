from nonebot import get_driver
setu_path = get_driver().config.setu_path

def save_img(content, pid: str, p: str, r18: bool = False):
    path = f"{'setu' if not setu_path else setu_path}{'r18' if r18 else '' }/{pid}_{p}.jpg"
    with open(path, "wb") as f:
        f.write(content)
