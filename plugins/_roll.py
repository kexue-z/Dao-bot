from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot, Event
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
import random

roll = on_command('r', priority=1)

@roll.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    temp = str(event.get_message()).strip()
    print(temp)
    if "d" in temp:
        _in = temp.split("d")
        D = []
        if int(_in[0]) <= 1000 and int(_in[1])<=1000:
            for i in range(int(_in[0])):
                _roll = random.randint(1,int(_in[1]))
                D.append(_roll)
            _out = str(_in[0]) + "D" + str(_in[1]) + "="
            for i in range(len(D)):
                _out += str(D[i])
                if i != len(D)-1:
                    _out += "+"
            sum = 0
            for i in range(len(D)):
                sum += int(D[i])
            msg = "你摇到了——\n"
            msg += _out + "=" +str(sum)
        else:
            msg = "太大了！装不下了！555~"
    # elif "+" in temp:
    #     print("有+")
    else:
        # print("没了")
        _in = temp.split(' ')
        r_range = _in[0].split('-')
        r_from = int(r_range[0])
        r_to = int(r_range[1])+1

        try:
            count = int(_in[1])
        except:
            count = 1

        if r_from >= 1000 or r_to >= 1000:
            msg = '太大了！装不下了！555~' 
        else:
            li = list()
            for i in range(r_from, r_to):
                li.append(i)

            _out = str(random.sample(li, count))
            msg  = '你摇到了——\n'
            msg += _out

    await bot.send(event, message=msg)
