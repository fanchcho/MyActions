## 企鹅读书教程
### 抓包
需要自行使用代理软件获取 书籍 `url` ， `headers` 和 `body`
* `MitM` 添加 `hostname=mqqapi.reader.qq.com`
* 添加改写
    ```
    圈x
    #企鹅读书获取更新body
    https:\/\/mqqapi\.reader\.qq\.com\/log\/v4\/mqq\/track url script-request-body https://raw.githubusercontent.com/ziye12/JavaScript/master/Task/qqreads.js
    #企鹅读书获取时长cookie
    https:\/\/mqqapi\.reader\.qq\.com\/mqq\/addReadTimeWithBid? url script-request-header https://raw.githubusercontent.com/ziye12/JavaScript/master/Task/qqreads.js

    loon
    //企鹅读书获取更新body
    http-request https:\/\/mqqapi\.reader\.qq\.com\/log\/v4\/mqq\/track script-path=https://raw.githubusercontent.com/ziye12/JavaScript/master/Task/qqreads.js,requires-body=true, tag=企鹅读书获取更新body
    //企鹅读书获取时长cookie
    http-request https:\/\/mqqapi\.reader\.qq\.com\/mqq\/addReadTimeWithBid? script-path=https://raw.githubusercontent.com/ziye12/JavaScript/master/Task/qqreads.js, requires-header=true, tag=企鹅读书获取时长cookie

    surge
    //企鹅读书获取更新body
    企鹅读书获取更新body = type=http-request,pattern=https:\/\/mqqapi\.reader\.qq\.com\/log\/v4\/mqq\/track,script-path=https://raw.githubusercontent.com/ziye12/JavaScript/master/Task/qqreads.js,
    //企鹅读书获取时长cookie
    企鹅读书获取时长cookie = type=http-request,pattern=https:\/\/mqqapi\.reader\.qq\.com\/mqq\/addReadTimeWithBid?,script-path=https://raw.githubusercontent.com/ziye12/JavaScript/master/Task/qqreads.js,
    ``` 
* 进**书库**选择一本书，看 `10` 秒以下，然后退出，获取书籍 `url` 和 `headers` 以及 `body`
### 修改配置文件
* 无论你用 `vps` 还是 `github action` ，都可以在目录 `./config/config.yml.example` 下找到配置文件模板 
* 在 `jobs` 下面找到 `qq_read` 任务，前面几个参数就是该任务的基本设置，自己看注释。在最后一个 `ACCOUNT` 参数下面填写你的账号信息，将先前抓到的获取书籍 `url` 和 `headers` 以及 `body` 对应填入配置文件里面的 `BOOK_URL`，`HEADERS` 和 `BODY`，剩下两个 `WITHDRAW` 和 `HOSTING_MODE` 参数看配置文件注释，填写只存在三种可能 `true,ture/true,false/false,false` （注意冒号后面的空格，不要带引号！）
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
  qq_read:
    # 使用前请阅读 https://raw.githubusercontent.com/TNanko/Scripts/master/scripts/qq_read.py 前30行使用说明
    enable: false # true 启用脚本； false 不启用脚本（默认不启用脚本）
    version: 1.1.0
    skip_check_script_version: false # 默认不跳过版本检测
    notify: false # true 启用消息推送； false 不启用消息推送（默认不发消息推送）
    notify_mode:  # 如果全都配置了，可以根据自身需求进行消息推送方式的选择，不需要的可以注释掉或者删除。由于 bark 消息长度的限制，不推荐 bark
      - bark
      - telegram_bot
      - dingding_bot
      - server_chan
    parameters:
      UPLOAD_TIME: 5 # 每次上传阅读时长（单位分钟）
      MAX_READ_TIME: 600 # 每日最大阅读时长（单位分钟）
      ACCOUNTS:
          # 多账号，将下面三个参数复制一遍，例子已经写好自行替换，注意冒号后面的空格，空格，空格！（建议在文本编辑器上输入）。
          # 进书库选择一本书，阅读几秒钟，将抓到的 headers ， body 和 书籍 url ，分别填到下方的 HEADERS ， BODY 和 BOOK_URL （注意冒号后面的空格，不要带引号！）
        - HEADERS: {"ywsession":"08nexxxxxxxxxx6kn6hx","Cookie":"ywguid=2xxxxxxxx8;ywkey=ywbxxxxxurwjS;platform=ios;channel=mqqmina;mpVersion=0.30.0;qq_ver=8.4.17;os_ver=iOS 14.2;mpos_ver=1.21.0;platform=ios;openid=B9A021EXXXXXXXXXXX18348A2F779","Connection":"keep-alive","Content-Type":"application/json","Accept":"*/*","Host":"mqqapi.reader.qq.com","User-Agent":"QQ/8.4.17.638 CFNetwork/1206 Darwin/20.1.0","Referer":"https://appservice.qq.com/1110657249/0.30.0/page-frame.html","Accept-Language":"zh-cn","Accept-Encoding":"gzip, deflate, br","mpversion":"0.30.0"}
          BODY: {"common":{"appid":1xxxxxx94,"areaid":5,"qq_ver":"8.4.17","os_ver":"iOS 14.1","mp_ver":"0.31.0","mpos_ver":"1.21.0","brand":"iPhone","model":"iPhone 12<iPhone13,2>","screenWidth":390,"screenHeight":844,"windowWidth":390,"windowHeight":761,"openid":"7E97DE3XXXXXXXXXXXX6C64DE9","guid":xxxxxxxxxx,"session":"d06xxxxxxxxxxxsc8w","scene":1132,"source":"wza0xxxxxxx002","hasRedDot":"false","missions":-1,"caseID":-1},"dataList":[{"click1":"bookDetail_bottomBar_read_C","click2":"bookDetail_chapter_slide_C","route":"pages/book-read/index","refer":"pages/book-detail/index","options":{"bid":"34207118","cid":"1"},"dis":1607349651957,"ext6":93,"eventID":"bookRead_show_I","type":"shown","ccid":1,"bid":"34207118","bookStatus":0,"bookPay":1,"chapterStatus":0,"ext1":{"font":18,"bg":0,"pageMode":1},"from":"bookLib2_bookList_bookClick_C_0_34207118"}]}
          BOOK_URL: https://mqqapi.reader.qq.com/mqq/addReadTimeWithBid?scene=3001&refer=-1&bid=30544815&readTime=2685&read_type=0&conttype=1&read_status=0&chapter_info=[{"65":{"readTime":2685,"pay_status":0}}]&sp=-1
          WITHDRAW: false  
          HOSTING_MODE: false 
        - HEADERS: {"ywsession":"08nexxxxxxxxxx6kn6hx","Cookie":"ywguid=2xxxxxxxx8;ywkey=ywbxxxxxurwjS;platform=ios;channel=mqqmina;mpVersion=0.30.0;qq_ver=8.4.17;os_ver=iOS 14.2;mpos_ver=1.21.0;platform=ios;openid=B9A021EXXXXXXXXXXX18348A2F779","Connection":"keep-alive","Content-Type":"application/json","Accept":"*/*","Host":"mqqapi.reader.qq.com","User-Agent":"QQ/8.4.17.638 CFNetwork/1206 Darwin/20.1.0","Referer":"https://appservice.qq.com/1110657249/0.30.0/page-frame.html","Accept-Language":"zh-cn","Accept-Encoding":"gzip, deflate, br","mpversion":"0.30.0"}
          BODY: {"common":{"appid":1xxxxxx94,"areaid":5,"qq_ver":"8.4.17","os_ver":"iOS 14.1","mp_ver":"0.31.0","mpos_ver":"1.21.0","brand":"iPhone","model":"iPhone 12<iPhone13,2>","screenWidth":390,"screenHeight":844,"windowWidth":390,"windowHeight":761,"openid":"7E97DE3XXXXXXXXXXXX6C64DE9","guid":xxxxxxxxxx,"session":"d06xxxxxxxxxxxsc8w","scene":1132,"source":"wza0xxxxxxx002","hasRedDot":"false","missions":-1,"caseID":-1},"dataList":[{"click1":"bookDetail_bottomBar_read_C","click2":"bookDetail_chapter_slide_C","route":"pages/book-read/index","refer":"pages/book-detail/index","options":{"bid":"34207118","cid":"1"},"dis":1607349651957,"ext6":93,"eventID":"bookRead_show_I","type":"shown","ccid":1,"bid":"34207118","bookStatus":0,"bookPay":1,"chapterStatus":0,"ext1":{"font":18,"bg":0,"pageMode":1},"from":"bookLib2_bookList_bookClick_C_0_34207118"}]}
          BOOK_URL: https://mqqapi.reader.qq.com/mqq/addReadTimeWithBid?scene=3001&refer=-1&bid=30544815&readTime=2685&read_type=0&conttype=1&read_status=0&chapter_info=[{"65":{"readTime":2685,"pay_status":0}}]&sp=-1
          WITHDRAW: true
          HOSTING_MODE: false 
        - HEADERS: {"ywsession":"08nexxxxxxxxxx6kn6hx","Cookie":"ywguid=2xxxxxxxx8;ywkey=ywbxxxxxurwjS;platform=ios;channel=mqqmina;mpVersion=0.30.0;qq_ver=8.4.17;os_ver=iOS 14.2;mpos_ver=1.21.0;platform=ios;openid=B9A021EXXXXXXXXXXX18348A2F779","Connection":"keep-alive","Content-Type":"application/json","Accept":"*/*","Host":"mqqapi.reader.qq.com","User-Agent":"QQ/8.4.17.638 CFNetwork/1206 Darwin/20.1.0","Referer":"https://appservice.qq.com/1110657249/0.30.0/page-frame.html","Accept-Language":"zh-cn","Accept-Encoding":"gzip, deflate, br","mpversion":"0.30.0"}
          BODY: {"common":{"appid":1xxxxxx94,"areaid":5,"qq_ver":"8.4.17","os_ver":"iOS 14.1","mp_ver":"0.31.0","mpos_ver":"1.21.0","brand":"iPhone","model":"iPhone 12<iPhone13,2>","screenWidth":390,"screenHeight":844,"windowWidth":390,"windowHeight":761,"openid":"7E97DE3XXXXXXXXXXXX6C64DE9","guid":xxxxxxxxxx,"session":"d06xxxxxxxxxxxsc8w","scene":1132,"source":"wza0xxxxxxx002","hasRedDot":"false","missions":-1,"caseID":-1},"dataList":[{"click1":"bookDetail_bottomBar_read_C","click2":"bookDetail_chapter_slide_C","route":"pages/book-read/index","refer":"pages/book-detail/index","options":{"bid":"34207118","cid":"1"},"dis":1607349651957,"ext6":93,"eventID":"bookRead_show_I","type":"shown","ccid":1,"bid":"34207118","bookStatus":0,"bookPay":1,"chapterStatus":0,"ext1":{"font":18,"bg":0,"pageMode":1},"from":"bookLib2_bookList_bookClick_C_0_34207118"}]}
          BOOK_URL: https://mqqapi.reader.qq.com/mqq/addReadTimeWithBid?scene=3001&refer=-1&bid=30544815&readTime=2685&read_type=0&conttype=1&read_status=0&chapter_info=[{"65":{"readTime":2685,"pay_status":0}}]&sp=-1
          WITHDRAW: true
          HOSTING_MODE: true 
```
