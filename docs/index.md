<div align="center">
  <img width="200" src="./images/dao-bot.png"/>
</div>

# 简介

- 这是一个由 [Nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 驱动的屑岛风 bot
- 由 kexue 维护，作为一个业余练手的项目
- 项目地址 💩 [kexue-z/Dao-bot](https://github.com/kexue-z/Dao-bot)
- 使用`[]` 为必须参数，使用`{}`为可选参数
- 直接在顶部评论区或者在选中任意文本即可反馈
- 其他问题联系 QQ`278220060`

> 部分指令需要添加指令头 `/ . 。! ！` 才能正确触发
> 某些特定指令不需要
> 带 `*` 表示 **不需要** 指令头或有其它指令

# 功能介绍

## 插件管理器

- 参考 [nonepkg/nonebot-plugin-manager](https://github.com/nonepkg/nonebot-plugin-manager)
- 权限为： `群聊群主` `群聊管理员` `私聊`
- 列出当前所有插件列表和启用情况
- 指令： `/npm ls`
- 禁用当前会话插件（需要权限）
  - 指令：`/npm block [plugin] ...`
- 启用当前会话插件（需要权限）
  - 指令：`/npm unblock [plugin] ...`

## MC 服务器状态查询和控制

- 指令：`/mc`
  - 查询科宝的 MC 服务器地址
- 指令: `/mcsm on|off|restart [服务器名字]`
  - 对服务器进行控制
  - 需要验证码
- 指令: `/mcc`
  - 对 MC 服务器发送指令，依赖于 MCSM 的后台
- 指令: `/mcadd`
  - 添加 MC 服务器，依赖于 MCSM
- 指令: `/mcdel`
  - 删除 MC 服务器

## 禁言通知

- 发送消息来提示禁言和解除禁言事件
- 与禁言功能不会同时触发

## \*天气查询

- 查询根据输入地区/城市名获取对应 7 天内天气
- 使用和风天气 API
- 指令： `天气` + `[地区]`
- 指令： `[地区]` + `天气`

## \*自动消息回复

- 参考 [kexue-z/nonebot-plugin-word-bank2](https://github.com/kexue-z/nonebot-plugin-word-bank2)
- 管理员可通过指令添加常见问题的回复
- 设置词条命令由`问句`和`答句`组成。设置之后, 收到`消息`时触发。并非所有人都可以设置词条, 详见[权限](#permission)
- 格式`[模糊|全局|正则|@]问...答...`

  - `模糊|正则` 匹配模式中可任性一个或`不选`, `不选` 表示 `全匹配`
  - `全局`, `@` 可与以上匹配模式组合使用

- 教学中可以使用换行

  - 例如
    ```
    问
    123
    答
    456
    ```

- 问答句中的首首尾空白字符会被自动忽略

- 私聊好友个人也可以建立属于自己的词库, 可以实现类似备忘录的功能

### 问句选项

- `问...答...` 全匹配模式, 必须全等才能触发答

- `模糊问...答...` 当`问句`出现在`消息`里时则会触发

- `正则问...答...`, 当`问句`被`消息`正则捕获时则会匹配
- 例如: 正则问[他你]不理答你被屏蔽了

  | 消息     | 回复       |
  | -------- | ---------- |
  | 他不理   | 你被屏蔽了 |
  | 他不理我 | 你被屏蔽了 |
  | 你不理我 | 你被屏蔽了 |

- `全局问...答...`, 在所有群聊和私聊中都可以触发, 可以和以上几种组合使用

  - 例如: `全局模糊问 晚安 答 不准睡`

- `@问...答...`, 只有 `event.tome` 时才会触发，如被@、被回复时或在私聊中，可以和以上几种组合使用

  - 例如: `全局模糊@问 晚安 答 不准睡`

- 问句可包含`at` 即在 QQ 聊天中手动 at 群友
  - 建议只在`问...答...`中使用
  - 例如: `问 @这是群名称 答 老婆!`

#### 答句选项

- `/at` + `qq号`, 当答句中包含`/at` + `qq号`时将会被替换为@某人

  - 例如: `问 群主在吗 答 /at 123456789在吗`

- `/self`, 当答句中包含`/self`时将会被替换为发送者的群昵称

  - 例如: `问 我是谁 答 你是/self` (群昵称为: 我老婆)

- `/atself`, 当答句中包含`/atself`时将会被替换为@发送者
  - 例如: `问 谁是牛头人 答 @这是群昵称`

### 删除词条

- `删除[模糊|全局|正则|@]词条` + 需要删除的`问句`

  - 例如: `删除全局模糊@词条 你好`

- 以下指令需要结合自己的`COMMAND_START` 这里为 `/`

- 删除词库: 删除当前群聊/私聊词库

  - 例如: `/删除词库`

- 删除全局词库

  - 例如: `/删除全局词库`

- 删除全部词库

  - 例如: `/删除全部词库`

- <span id="permission">权限</span>

|              | 群主 | 群管理 | 私聊好友 | 超级用户 |
| ------------ | ---- | ------ | -------- | -------- |
| 增删词条     | O    | O      | O        | O        |
| 增删全局词条 | X    | X      | X        | O        |
| 删除词库     | O    | O      | O        | O        |
| 删除全局词库 | X    | X      | X        | O        |
| 删除全部词库 | X    | X      | X        | O        |

## 通用订阅推送 RSS

- 参考 [felinae98/nonebot-bison](https://github.com/felinae98/nonebot-bison)
- 可订阅 bilibili 动态、微博动态
- 可订阅 [https://docs.rsshub.app/](https://docs.rsshub.app/) 中的所有支持的 RSS 订阅源和其他源
- 定期爬取指定网站内容并发布
- 控制指令仅限群主和管理员
- 指令 `/添加订阅`
  - 需要通过选择来添加 UID 才能使用
- 各平台 UID
  - weibo
    - 对于一般用户主页`https://weibo.com/u/6441489862?xxxxxxxxxxxxxxx`，`/u/`后面的数字即为`uid`
    - 对于有个性域名的用户如：`https://weibo.com/arknights`，需要点击左侧信息标签下`更多`，链接为`https://weibo.com/6279793937/about`，其中中间数字即为`uid`
  - Bilibili
    - 主页链接一般为`https://space.bilibili.com/161775300?xxxxxxxxxx`，数字即为 uid
  - RSS
    - RSS 链接即为 uid
    - RSS 链接获取方式见下方 **RSS 链接获取方式（RSS 阅读器通用）**
- 指令 `/删除订阅`
  - 按照提示操作即可

## RSS 链接获取方式（RSS 阅读器通用）

- 什么是 RSS **你不会百度吗？**
- 自建 RSS 服务器链接 `https://kexue.io:1200`
- 部分需要配置的 RSS 源需要 @kexue 来进行配置

1. 访问 [https://docs.rsshub.app/](https://docs.rsshub.app/)
   - 如果网站被墙建议 🪜
   - 或者直接通过 GitHub [获取文档](https://github.com/DIYgod/RSSHub/tree/master/docs)
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

## WolframAlpha 搜索

- 参考 [MeetWq/mybot](https://github.com/MeetWq/mybot)
- 这是什么？
  - 一个高级的搜索引擎
  - 能计算、思考，具体 B 站有教程
- 指令： `/wolfram [你的问题]`
  - 返回结果为图片
- 每月限制调用次数`2000`
  - 希望你能问一下高级的问题

## 退群

- 屑岛风 bot 要退群了吗？
- 指令 `/dismiss` / `/退群`
- 仅群主或管理员才可使用

## \*土命笑话

- 发送一个土命笑话
- 模糊匹配 `命运笑话`, `土命笑话`, `D2笑话`, `d2笑话`

# 发病

- 发一个病
- 指令 `/发病 xxx`

## 猫 GIF

- 随机猫猫 GIF
- 指令 `/猫` `/来个猫猫` `/猫猫` `/猫图`

# TODO

- [x] 摸鱼

# 特别感谢

- 辛苦自己了
- Nonebot 社区神一般的群友
- [nonebot/nonebot2](https://github.com/nonebot/nonebot2/)：简单好用，扩展性极强的 Bot 框架
- [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：更新迭代快如疯狗的  [OneBot](https://github.com/howmanybots/onebot/blob/master/README.md) Golang 原生实现
