## bilibili签到教程

### 获取 Cookie

* 访问网站 http://live.bilibili.com/ 并登录你的 `bilibili` 账号
* 获取 Cookie
    * 以 Chrome 浏览器为例，按 F12 进入调试模式，在调试窗口上方选择 Network ，刷新一下网页，随意点下方一个文件，然后找到 Cookie 并复制到配置文件中参数 COOKIE
    * 如果你使用 圈x 、 Surge 、 Loon 或者 Shadowrocket 等代理软件，可以使用访问网页 https://github.com/chavyleung/scripts/tree/master/bilibili 并使用此网页提供的方法来获取 Cookie

### 修改配置文件

* 无论你用 `vps` 还是 `github action` ，都可以在目录 `./config/config.yml.example` 下找到配置文件模板 
* 在 `jobs` 下面找到 `bilibili` 任务，前面几个参数就是该任务的基本设置，自己看注释。在最后一个 `ACCOUNT` 参数下面填写填写你的 `COOKIE`
* 写完配置文件后在[在线检验yaml语法](https://www.toolfk.com/tool-format-yaml)检验一下 `yaml` 语法是否规范，当然你可以百度 `Google` 其他的在线检验网站。

## 关于多账号设置

下面给一个三账号的例子，剩下的自己举一反三。一定要检验 `yaml` 语法！一定要检验 `yaml` 语法！一定要检验 `yaml` 语法！
```yaml
name: TNanko's Scripts Config File
version: 1.2.3
skip_check_config_version: false # 默认不跳过配置文件的版本检测

# 消息推送
notify:
  enable: true # true 开启消息推送； false 关闭消息推送 （默认所有脚本开启消息推送）
  type:
    # 建议只填写一两个或者全部填写后设置对应脚本任务中的 notify_mode 参数
    bark:
      # ios 在 app store 下载 bark app，bark 推送 url 为 https://api.day.app/xxxxxxxxxxx/这里改成你自己的推送内容，则 xxxxxxxxxxx 为你的 bark 机器码
      BARK_MACHINE_CODE:
    telegram_bot:
      # 暂时自行百度google
      TG_BOT_TOKEN:
      TG_USER_ID:
    dingding_bot:
      # 钉钉机器人，参考教程：https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq 在"安全设置"中选择"加签"（必须勾选），其他不懂不要勾选
      DD_BOT_ACCESS_TOKEN:
      DD_BOT_SECRET:
    server_chan:
      # 未测试
      # ServerChan，参考教程：http://sc.ftqq.com/3.version
      SCKEY:

# 脚本配置信息
jobs:
  bilibili:
    # 使用前请阅读 https://raw.githubusercontent.com/TNanko/Scripts/master/scripts/bilibil.py 前12行使用说明
    enable: false # true 启用脚本； false 不启用脚本（默认不启用脚本）
    version: v1.0.5
    skip_check_script_version: false # 默认不跳过版本检测
    notify: true # true 启用消息推送； false 不启用消息推送（默认发消息推送）
    notify_mode:  # 如果全都配置了，可以根据自身需求进行消息推送方式的选择，不需要的可以注释掉或者删除。推荐 bark
      - bark
      - telegram_bot
      - dingding_bot
      - server_chan
    scripts_filename: 'bilibili.py'
    schedule:
      cron: '10 1 * * *'
    parameters:
      ACCOUNTS:
        - COOKIE: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        - COOKIE: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        - COOKIE: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
