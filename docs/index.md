<div align="center">
  <img width="200" src="./images/dao-bot.png"/>
</div>

# 简介

- 这是一个由 [Nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 驱动的屑岛风 bot
- 由 kexue 维护，作为一个业余练手的项目
- 项目地址 💩 [https://github.com/kexue-z/Dao-bot](https://github.com/kexue-z/Dao-bot)
- 使用`[]` 为必须参数，使用`{}`为可选参数
- 直接在顶部评论区或者在选中任意文本即可反馈
- 其他问题联系 QQ`278220060`
  > 部分指令需要添加指令头 `/ . 。! ！` 才能正确触发
  > 某些特定指令不需要
  > {.is-info}

# 功能介绍

## 插件管理器

- 参考 [https://github.com/nonepkg/nonebot-plugin-manager](https://github.com/nonepkg/nonebot-plugin-manager)
- 列出当前所有插件列表和启用情况
- 指令： `npm ls`
- 禁用当前会话插件（需要权限）
  - 指令：`npm block plugin...`
- 启用当前会话插件（需要权限）
  - 指令：`npm unblock plugin...`

## 决定

- 输入一系列内容，并返回一个随机结果
- 指令： `/决定｜选择 {内容}` （内容需要用空格分开）
- 例如： `/决定 睡大觉 玩游戏 学习` 返回`屑岛风bot认为你应该选择：睡大觉`
- 当不输入内容时则会询问`[内容]` 此时可不输入`/决定` 作为指令头

## MC 服务器状态查询和控制

- 指令：`/mc 服务器地址[:端口]`
  - 服务器地址可以是 ip 或域名，端口不填写则默认 25565
- 指令: `/开服` | `/mcon` | `/打开服务器` + `[服务器ID]`
  - 需要验证码
- 指令: `/关服` | `/mcoff` | `/关闭服务器` + `[服务器ID]`
  - 需要验证码
- 指令: `/重启服` | `/mcrestart` | `/重启服务器` + `[服务器ID]`
  - 需要验证码

## 禁言

- 群管理员或特殊指定人员可通过发送群聊来禁言用户
- 方便部分 QQ 版本没有禁言按钮的客户端使用
- 需要 bot 为管理员身份
- 私聊中不可用~~废话~~
- 指令：`/m` | `/mute` | `/禁言` + `[at指定用户]` + `{时长}`
  - 需要 at 而不是复制粘贴文本
  - 时长单位为分钟，默认为 10

## 禁言通知

- 发送消息来提示禁言和解除禁言事件
- 与禁言功能不会同时触发

## 色图（~~基础功能~~）

{.is-warning}

- 发送随机色图。可指定关键词标签
- 标签为 Pixiv 作品下的标签
- 指令 `(setu|色图|涩图|来点色色|色色)\s?(r18)?\s?(.*)?`
  - 获取~~特殊~~色图
    - 仅限私聊
- 内置 60s CD
- 某些图片可能发送不成功，为腾讯风控或 API 错误
- API [https://api.lolicon.app/](https://api.lolicon.app/)

## 天气查询

- 查询根据输入地区/城市名获取对应 3 天内天气
- 使用和风天气 API
- 指令： `天气` + `[地区]`
- 指令： `[地区]` + `天气`

## 自动消息回复

- 参考 [https://github.com/Joenothing-lst/word-bank](https://github.com/Joenothing-lst/word-bank)
- 管理员可通过指令添加常见问题的回复
- 增加词条
  - 全匹配问答
    - 指令：`问[问题]答[回答]`
    - 例子：`问他不理答你被屏蔽了`
    - 运行结果：`他不理` → `你被屏蔽了`
  - 模糊问答
    - 指令：`模糊问[问题]答[回答]`
    - 例子：`模糊问他不理答你被屏蔽了`
    - 运行结果：`他不理` → `你被屏蔽了` | `他不理我` → `你被屏蔽了` | `他不理他` → `你被屏蔽了`
  - 回答部分格式
    - `/at` + `[QQ号]`
      - 当答句中包含 `/at` + `qq号`时将会被替换为@某人
      - 例子：`问群主在吗答/at123456789在吗`
      - 运行结果：`群主在吗` → `@群主 在吗`
    - `/self`
      - 当答句中包含 `/self`时将会被替换为发送者的群昵称
      - 例子：`问我是谁答你是/self`
      - 运行结果：`我是谁` → `你是孤独科宝。`
    - `/atself`
      - 当答句中包含 `/atself`时将会被替换为发送者的群昵称
      - 例子：`问我是谁答你是/atself`
      - 运行结果：`我是谁` → `你是@孤独科宝。`
    - `/ban`
      - 当答句中包含`/ban`后紧跟数字时将会禁言发送者
      - 单位为秒，默认为 300s
      - 例子：`问你好答/ban30你将被禁言30秒`
      - 运行结果：`你好` → `你将被禁言30秒` `你已被管理员禁言30秒`
- 删除词条
  - 指令：`/删除词条`+`[问题]`
- 删除词库
  - 指令：`/删除词库`
  - 仅限群主

## 以图搜源

- 适用于二次元图
- 由于搜图结果较多，**建议私聊使用**
- 可使用的搜图接口 `nao` `iqdb` `ascii2d` 可缩写为 `asc`
- 指令：`/搜图`
  - 群聊中使用需要 at bot 才能触发，私聊可直接发送
- 指令：`/上一张` `/这是什么` `上一张图是什么`
  - 将改用户发送的上一张图片直接进行搜图
  - 不需要 at bot
  - 默认搜图接口为 `nao`

## COC 骰子娘

- 参考 [https://github.com/abrahum/nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer)
- 输入 `.help` 获取帮助信息
- 指令详解

  ```
  .r[dah#bp] a_number [+/-]ex_number
  ```

  - d：骰子设定指令，标准格式为 xdy ， x 为骰子数量 y 为骰子面数， x 为 1 时可以省略， y 为 100 时可以省略；
  - a：检定指令，根据后续 a_number 设定数值检定，注意 a 必须位于 a_number 之前，且 a_number 前需使用空格隔开；
  - h：暗骰指令，骰子结构将会私聊发送给该指令者；（没测试过非好友，可以的话先加好友吧）
  - #：多轮投掷指令， # 后接数字即可设定多轮投掷，注意 # 后数字无需空格隔开；
  - b：奖励骰指令，仅对 D100 有效，每个 b 表示一个奖励骰；
  - p：惩罚骰指令，同奖励骰；
  - +/-：附加计算指令，目前仅支持数字，同样无需空格隔开。

  > 举几个栗子：
  >
  > - `.r#2bba 70`：两次投掷 1D100 ，附加两个奖励骰，判定值为 70；
  > - `.rah`：D100 暗骰，由于没有 a_number 参数，判定将被忽略；
  > - `.ra2d8+10 70`：2D8+10，由于非 D100，判定将被忽略。

  以上指令理论上均可随意变更顺序并嵌套使用，如果不能，就是出 bug 了*(:3」∠)*

  ```
  .sc success/failure [san_number]
  ```

  - success：判定成功降低 san 值，支持 x 或 xdy 语法（ x 与 y 为数字）；
  - failure：判定失败降低 san 值，支持语法如上；
  - san_number：当前 san 值，缺省 san_number 将会自动使用保存的人物卡数据。

  ```
  .en skill_level
  ```

  - skill_level：需要成长的技能当前等级。

  ```
  .coc [age]
  ```

  - age：调查员年龄，缺省 age 默认年龄 20

  > 交互式调查员创建功能计划中

  ```
  .set [attr_name] [attr_num]
  ```

  - attr_name：属性名称，例:name、名字、str、力量
  - attr_num：属性值
  - **可以单独输入 .set 指令，骰娘将自动读取最近一次 coc 指令结果进行保存**

  | 属性名称 | 缩写 |
  | :------: | :--: |
  |   名称   | name |
  |   年龄   | age  |
  |   力量   | str  |
  |   体质   | con  |
  |   体型   | siz  |
  |   敏捷   | dex  |
  |   外貌   | app  |
  |   智力   | int  |
  |   意志   | pow  |
  |   教育   | edu  |
  |   幸运   | luc  |
  |   理智   | san  |

  ```
  .show[s] [@xxx]
  ```

  - .shows 查看技能指令
  - 查看指定调查员保存的人物卡，缺省 at 则查看自身人物卡

  ```
  .sa [attr_name]
  ```

  - attr_name：属性名称，例:name、名字、str、力量

  ```
  .del [c|card|xxx]
  ```

  - c：清空暂存的人物卡
  - card：删除使用中的人物卡(慎用)
  - xxx：其他任意技能名
  - 以上指令支持多个混合使用，多个参数使用空格隔开

## Bilibili QQ 小程序转换为链接

- 为了照顾某些特殊客户端，将 QQ 小程序转为链接
- 无指令，发送 B 站视频小程序即可

## 通用订阅推送（香港记者）

- 参考 [https://github.com/felinae98/nonebot-hk-reporter](https://github.com/felinae98/nonebot-hk-reporter)
- 可订阅 bilibili 动态、微博动态
- 可订阅 [https://docs.rsshub.app/](https://docs.rsshub.app/) 中的所有支持的 RSS 订阅源和其他源
- 定期爬取指定网站内容并发布
- 控制指令仅限群主和管理员
- 指令 `/添加订阅`
  - 需要通过选择来添加 UID 才能使用
- 各平台 UID
  - weibo
    - 对于一般用户主页`https://weibo.com/u/6441489862?xxxxxxxxxxxxxxx`，`/u/`后面的数字即为`uid`
    - 对于有个性域名的用户如：`https://weibo.com/arknights`，需要点击左侧信息标签下“更多”，链接为`https://weibo.com/6279793937/about`，其中中间数字即为`uid`
  - Bilibili
    - 主页链接一般为`https://space.bilibili.com/161775300?xxxxxxxxxx`，数字即为 uid
  - RSS
    - RSS 链接即为 uid
    - RSS 链接获取方式见下方 **RSS 链接获取方式（RSS 阅读器通用）**
- 指令 `/删除订阅`
  - 按照提示操作即可

## RSS 链接获取方式（RSS 阅读器通用）

- 什么是 RSS → 百度
- 自建 RSS 服务器链接 `https://kexue.io:1200`
- 部分需要配置的 RSS 源需要 @kexue 来进行配置

1. 访问 [https://docs.rsshub.app/](https://docs.rsshub.app/)
   - 如果网站被墙建议 🪜
   - 或者直接通过 GitHub 获取文档 [https://github.com/DIYgod/RSSHub/tree/master/docs](https://github.com/DIYgod/RSSHub/tree/master/docs)
2. 找到相应分类
3. 获取路由 并填写相应参数
   - 例如：`/36kr/news/:caty`
   - 将 `:caty` 替换为文档中的参数 `latest`
   - 结果是 `/36kr/news/latest`
4. 组合链接
   - 最终组合结果为 `https://kexue.io:1200/36kr/news/latest`
   - 将上述结果通过发送到群聊中即可添加
   - 该链接对于 RSS 阅读器同样有效

- 部分 RSS 链接

  ```
  https://kexue.io:1200/cneb/yjxx 预警信息_国家应急广播网
  https://kexue.io:1200/anigamer/new_anime 番剧更新
  https://kexue.io:1200/36kr/news/latest 36氪最新新闻
  https://kexue.io:1200/3dm/news 3DM新闻中心
  ```

## 模拟抽卡

- 参考 [https://github.com/HibiKier/nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw)
- 支持的抽卡和指令
  - `原神[武器|角色] [1~10][抽|井]`
  - `方舟 [1~10][抽|井]`
  - `赛马娘{卡} [1~10][抽|井]`
  - `坎公骑冠剑 [1~10][抽|井]`
  - `公主连结|pcr|公主链接|公主连接 [1~10][抽|井]`
  - `碧蓝(航线){轻型|重型|特型} [1~10]抽`
  - `fgo [1~10]抽`
  - `阴阳师[1~10]抽`
- 其他指令
  - `重置原神抽卡`（重置保底）
  - `重载原神卡池`
  - `重载方舟卡池`
  - `重载赛马娘卡池`
  - `重载坎公骑冠剑卡池`
- 更新信息
  - `更新[明日方舟|原神|赛马娘|赛坎公骑冠剑|pcr|碧蓝航线|fgo|阴阳师]信息`
- 原版正则表达

  ```
  ' .* ?方舟[1-9|一][0-9]{0,2}[抽|井]'
  ' .* ?原神(武器|角色)?池?[1-9|一][0-9]{0,2}[抽|井]'
  ' .* ?马娘卡?[1-9|一][0-9]{0,2}[抽|井]'
  ' .* ?坎公骑冠剑武?器?[1-9|一][0-9]{0,2}[抽|井]'
  ' .* ?(pcr|公主连结|公主连接|公主链接|公主焊接)[1-9|一][0-9]{0,2}[抽|井]'
  ' .* ?碧蓝航?线?(轻型|重型|特型)池?[1-9|一][0-9]{0,2}[抽]'
  ' .* ?fgo[1-9|一][0-9]{0,2}[抽]'
  ' .* ?阴阳师[1-9|一][0-9]{0,2}[抽]'
  ```

## 你不会百度吗？？？

- 帮你百度，喜欢吗？
- 指令：`百度/baidu` + `关键词`
- 返回：**那肯定是百度啊???**

## WolframAlpha 搜索

- 参考 [MeetWq/mybot](https://github.com/MeetWq/mybot)
- 这是什么？
  - 一个高级的搜索引擎
  - 能计算、思考，具体 b 站有教程
- 指令： `/wolfram {-p} [你的问题]`
  - 可选：`-p` 表示返回结果为纯文本
  - 默认返回结果为图片
- 每月限制调用次数`2000`
  - 希望你能问一下高级的问题

## 新闻

- 获取每日新闻
- 指令： `/新闻 | /news`

## 点歌

- 参考 [MeetWq/mybot](https://github.com/MeetWq/mybot)
- 点歌
- 指令`/点歌|music {-s 平台} [关键词]`
  - 平台可选：`qq | netease | kugou | migu | bilibili`
  - 例如： `/点歌 -s netease Never Gonna Give You Up`

## EPIC 喜加一

- 参考 [monsterxcn/nonebot_plugin_epicfree](https://github.com/monsterxcn/nonebot_plugin_epicfree)
- 获取 EPIC 免费游戏
- 指令 `/epic喜加一`

## 管理员对话

- 参考 [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)
- 与管理员间接沟通
- 在群内 `@屑岛风bot [Msg]` 或者 `屑岛风 [Msg]`
- 管理指令：
  - `/t` -> 列出所有待回复消息
  - `/t [qq] [group] [text]` -> 回复指定用户
  - `/t [qq] [text]` -> 私聊用户
  - `/t -1 [group]` -> 在某群发送消息
  - `/t [id] [text]` -> 回复指定 id 的对话

## 二次元语录

- 参考 [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)
- 中二二次元语录，可给你前进的力量！！！
- 指令： `/二次元｜/二次元语录｜/语录`

## 广播

- 指令 `/广播-[内容]`
- 在群聊中发送广播
- TODO：
  - 添加群例外

## bilibili 番剧查询

- 指令 `/番剧 + [内容]`
  - 查询 bilibili 番剧
- 指令 `[时间]新番`
  - 查询番剧更新时间表
  - 时间词语: `今日` `明日` `周一~周日`
  - 例如 `周四新番`

## 跑团记录记录器

- 参考[thereisnodice/TRPGLogger](https://github.com/thereisnodice/TRPGLogger)

- 指令 `/log on` `/log off`
  - 记录聊天记录并上传

## 草图生成器

- 指令 `/5kcy` | `/5000兆元` | `/5000兆円` | `/5000choyen` `[上联] | [下联]`
- 生成草图 实例
  - <img width="250" src="./images/卡碧菊-牛头人.png"/>
- 指令 `/phlogo`|`/pornhub`|`/ph图标` `[text1] [text2]`
- 生成 ph 风格图标 实例
  - <img width="250" src="./images/屑岛风bot.png"/>
- 指令 `/nka` | `/诺基亚` `[text]`
- 生成诺基亚手机
  - <img width="250" src="./images/nka.png">

## 退群

- 屑岛风 bot 要退群了吗？
- 指令 `/dismiss` `/退群`
- 仅群主或管理员才可使用

## 二维码识别和生成

- 识别
  - 直接识别二维码中的信息，并转为文本发送
  - 指令 `qr` | `二维码` | `qrcode` `{图片}`
    - 图片可在触发指令后下一条发送
  - 指令 `pqr` | `前一二维码` | `pqrcode`
  - 识别上一条发送的图片中的二维码
  - TODO: ~~多个二维码识别~~ ，返回模板模板
- 生成
  - 还没做

## 青年大学习

- 获取青年大学习答案
- 参考[nonebot_plugin_youthstudy](https://github.com/ayanamiblhx/nonebot_plugin_youthstudy)
- 指令 `/青年大学习` `/大学习`

# 更新日志

- 7.3 添加了 RSS 服务器和消息聚合订阅功能
- 8.5 优化了色图发送机制
- 8.8 你不会百度吗？？？
- 8.9 添加 WolframAlpha 搜索引擎
- 8.12 添加每日新闻获取
- 8.18 添加点歌插件、优化色图风控机制
- 8.20 添加 epic 喜加一、管理员对话、广播功能、二次元语录
- 9.26 草图生成器
- 10.21 整改指令格式头为 `/ . 。! ！`
- 11.17 增加退群、另外一个草图生成

# TODO

- [x] 将天气模块修改为图片发送
- [x] 番剧更新（变成 RSS 订阅的万能工具）
- [x] 私聊获取 R18 图
- [x] 你不会自己百度吗？
- [ ] 在线代码运行
- [x] epic 限免
- [ ] 广播插件添加忽略功能
- [x] ph 风格图片生成
- [x] 天气插件更新

# 特别感谢

- 辛苦自己了
- Nonebot 社区神一般的群友

- [nonebot/nonebot2](https://github.com/nonebot/nonebot2/)：简单好用，扩展性极强的 Bot 框架
- [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：更新迭代快如疯狗的  [OneBot](https://github.com/howmanybots/onebot/blob/master/README.md) Golang 原生实现