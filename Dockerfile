# Description: Dockerfile for Python3.10

# 使用官方的Ubuntu 22.04镜像作为基础镜像
FROM ubuntu:22.04

# 设置环境变量，避免交互式配置
ENV DEBIAN_FRONTEND=noninteractive

# 替换 APT 源列表
RUN echo "deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse" >> /etc/apt/sources.list

# 更新软件包列表并安装 mysql
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y python3-pip python3-dev python3-venv libmysqlclient-dev mysql-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 初始化MySQL
COPY init.sh /docker-entrypoint-init.d/
COPY init.sql /docker-entrypoint-init.d/
COPY start.sh /docker-entrypoint-init.d/
COPY flask.sh /docker-entrypoint-init.d/
COPY requirements.txt /docker-entrypoint-init.d/
VOLUME ["/var/lib/mysql"]

RUN usermod -d /var/lib/mysql/ mysql
RUN bash /docker-entrypoint-init.d/init.sh

ENV FLASK_APP=bs
ENV FLASK_ENV=development

# 定义工作目录
WORKDIR /home/bs

# 暴露端口
# EXPOSE 8080
EXPOSE 5000

# 设置容器启动时运行的命令
CMD ["bash"]
