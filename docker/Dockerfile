FROM python:alpine
LABEL maintainer="Evine Deng <evinedeng@foxmail.com>"
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    HOME=/root \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    SCRIPTS_DIR="/Scripts"
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk --no-cache add -f bash \
                             coreutils \
                             git \
                             tzdata \
    && rm -rf /var/cache/apk/* \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple \
    && python -m pip install --upgrade pip \
    && git clone -b master https://github.com/TNanko/Scripts ${SCRIPTS_DIR} \
    && cd ${SCRIPTS_DIR} \
    && pip install -r requirements.txt \
    && cp ${SCRIPTS_DIR}/docker/entrypoint.sh /usr/local/bin/entrypoint.sh \
    && chmod 777 /usr/local/bin/entrypoint.sh
WORKDIR ${SCRIPTS_DIR}
ENTRYPOINT entrypoint.sh