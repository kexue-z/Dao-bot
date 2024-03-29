import re
import subprocess

from nonebot import on_command
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.rule import ArgumentParser
from nonebot.adapters.onebot.v11 import Bot, Event, Message

from plugins.wolfram.data_source import get_wolframalpha_text, get_wolframalpha_simple

__name__ = "wolfram"


description = "WolframAlpha计算知识引擎"
usage = "Usage:\n  wolfram {text}"
options = "Options:\n  -p, --plaintext 纯文本结果"
help = description + "\n" + usage + "\n" + options

wolfram_parser = ArgumentParser()
wolfram_parser.add_argument("-p", "--plaintext", type=int, default=2)
wolfram_parser.add_argument("equation", nargs="+")

wolfram = on_command("wolfram", aliases={"wolframalpha"}, priority=34)


@wolfram.handle()
async def _(bot: Bot, event: Event, arg: Message = CommandArg()):
    text = arg.extract_plain_text()
    logger.info(f"input={text}")
    # msg = await get_wolframalpha_simple(text)
    plaintext = False
    pattern = [r"-p +.*?", r".*? +-p", r"--plaintext +.*?", r".*? +--plaintext"]
    for p in pattern:
        if re.fullmatch(p, text):
            plaintext = True
            break
    text = text.replace("-p", "").replace("--plaintext", "").strip()
    if not text:
        await wolfram.finish(usage)

    if not re.fullmatch(r"[\x00-\x7F]+", text):
        # TODO 翻译功能无法实现
        text = subprocess.getoutput(f'trans -t en -brief -no-warn "{text}"').strip()
        if text:
            await wolfram.send("WolframAlpha 仅支持英文，将使用如下翻译进行搜索：\n" + text)
        else:
            await wolfram.finish("出错了，请稍后再试")

    if plaintext:
        msg = await get_wolframalpha_text(text)
    else:
        msg = await get_wolframalpha_simple(text)
    if not msg:
        await wolfram.finish("出错了，请稍后再试")

    await wolfram.send(message=msg)
    await wolfram.finish()
