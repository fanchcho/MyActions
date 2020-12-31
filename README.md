## 描述

一个使用 `Python` 语言写的薅羊毛脚本仓库，支持 `github action` 和 `linux/windows virtual private server` 

## 部署方式

**注意**：所有脚本任务都是未启用并且默认不发消息推送，请自行根据自身需求设置，配置文件采用 `yaml` 语法编写（注意空格），建议使用文本编辑器填写配置，以防格式错误！ 

最好写完配置文件后在[在线检验yaml语法](https://www.toolfk.com/tool-format-yaml)检验一下 `yaml` 语法是否规范，当然你可以百度 `Google` 其他的在线检验网站。

### 一、linux/windows virtual private server

* 安装环境
    ```
    # debian/ubuntu/armbian/OpenMediaVault等其他debian系
    apt-get install git python3 -y
    
    # CentOS/RedHat/Fedora等红帽系
    yum install git python3 -y
    ```
* 下载代码
    ```
    git clone https://github.com/TNanko/Scripts.git
    ```
* 部署脚本
    ```yaml
    # 进入脚本目录
    cd Scripts
    
    # 安装脚本需要的包
    pip3 install -r requirements.txt

    # 复制仓库下config/config.yml.example到config目录中，并重命名为config.yml
    cp ./config/config.yml.example ./config/config.yml

    # 编辑配置文件（推送和脚本配置，建议将配置文件下载到本地使用 Visual Studio Code/Sublime Text/Vim 等文本编辑器编辑）
    vi ./config/config.yml

    # 运行 setup.py 添加 cron 定时任务
    python3 setup.py
    ```

### 二、github action

* 添加一个 `secrets` - `CONFIG` ， `Value` 内容请复制目录下 `./config/config.yml.example` 所有内容。

* 填写对应的推送方式的 `key` 或者 `code`。

* 找到想要运行的脚本，设置对应的配置信息。

* 手动 `star` 一下仓库，看下 `Action` 是否正常运行。

* 定时同步仓库：添加一个 `secrets` - `PAT` ，[教程](https://www.jianshu.com/p/bb82b3ad1d11)。

### 三、Docker

1. 下载本仓库`config`文件夹下的`config.yml.example`文件到指定位置，并改名为`config.yml`，比如下载到`/appdata/tnanko`文件下，可如下操作：

    ```shell
    cd /appdata/tnanko
    wget --no-check-certificate https://raw.githubusercontent.com/TNanko/Scripts/master/config/config.yml.example -O config.yml
    ```

2. 修改刚刚下载好的`config.yml`，如何修改请见 [教程](docs/qq_read.md)，写完配置文件后在[在线检验yaml语法](https://www.toolfk.com/tool-format-yaml)检验一下 `yaml` 语法是否规范，当然你可以百度 `Google` 其他的在线检验网站。

3. 自行安装好Docker后部署容器，以刚刚修改的配置文件的路径`/appdata/tnanko`为例：

    ```shell
    docker run -dit \
    -v /appdata/tnanko/config.yml:/Scripts/config/config.yml `#配置文件保存目录，冒号左边是示例路径，以你实际路径为准` \
    -v /appdata/tnanko/log:/Scripts/log `#日志保存目录，冒号左边是示例路径，以你实际路径为准` \
    --name tnanko_scripts \
    --hostname tnanko_scripts \
    --restart always \
    evinedeng/tnanko_scripts
    ```

4. 完成，等着收钱吧。如果你想修改配置，只要不是改cron，直接改完`config.yml`就行了，无需重启容器什么的；但如果你想改cron，改完以后必须重启下容器，命令：`docker restart tnanko_scripts`

## 消息推送

目前支持 `ios bark app` ， `telegarm bot` ， `dingding bot` ， `serverChan` 四种方式推送消息。

打开推送方式：将 `config.yml` 里面 `notify` 选项中，参数 `enable` 设置为 `true`

## 支持的脚本任务

### 企鹅读书

* 使用脚本前务必看一遍教程，[脚本地址](https://raw.githubusercontent.com/TNanko/Scripts/master/scripts/qq_read.py)，[使用教程](https://github.com/TNanko/Scripts/blob/master/docs/qq_read.md)

* 此脚本使用 `Python` 语言根据[原js脚本](https://raw.githubusercontent.com/ziye12/JavaScript/master/Task/qqreads.js)重写，并在原有的基础上扩展了一些功能。

### `bilibili` 签到

* 使用脚本前务必看一遍教程，[脚本](https://raw.githubusercontent.com/TNanko/Scripts/master/scripts/bilibili.py)，[使用教程](https://github.com/TNanko/Scripts/blob/master/docs/bilibili.md)

## 关于版本

### 配置文件的版本

**版本号：v<主版本号>.<子版本号>.<阶段版本号>**
* 主版本号发生改变，表示代码框架改动较大，如果更新代码后，则必须更新配置文件；
* 子版本号发生改变，表示增加新功能或者新脚本，如果需要使用新脚本，则需要更新配置文件并重新配置；
* 阶段版本号发生改变，表示修复某个脚本的 `bug`，则根据对应脚本的版本号来决定是否需要更新配置文件。

### 脚本的版本

**版本号：v<主版本号>.<子版本号>.<阶段版本号>**
* 主版本号发生改变，大概率此脚本重新了，如果更新代码后，则必须更新配置文件；
* 子版本号发生改变，表示该脚本新增功能，如果需要使用新脚本，则需要更新配置文件并重新配置；
* 阶段版本号发生改变，表示修复某个脚本的 `bug`，不需要更新配置文件。
