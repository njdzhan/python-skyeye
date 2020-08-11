##############################################
# 基于centos7构建python3运行环境
# 构建命令: 在Dockerfile文件目录下执行 docker build -t python-centos:3.5 .
# 容器启动命令: docker run -itd --name python --restart always --privileged=true -v /root/dockers/python:/root/python -v /root/dockers/python/cron:/var/spool/cron python-centos:3.5 /usr/sbin/init
# 进入容器：docker exec -it python /bin/bash
##############################################
FROM centos:7
MAINTAINER han # 指定作者信息

#RUN 执行以下命令 
RUN mkdir /home/docker

#ADD  
ADD oracle.py /home/docker
EXPOSE 9800

RUN set -ex \
    # 预安装所需组件
    && yum install -y wget tar libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make initscripts \
    && wget http://192.168.121.244/Python-3.8.5.tgz \
    && tar -zxvf Python-3.8.5.tgz \
    && cd Python-3.8.5 \
    && ./configure prefix=/usr/local/python3 \
    && make \
    && make install \
    && make clean \
    && rm -rf /Python-3.8.5* \
    && yum install -y epel-release \
    && yum install -y python-pip
# 设置默认为python3
RUN set -ex \
    # 备份旧版本python
    && mv /usr/bin/python /usr/bin/python27 \
    && mv /usr/bin/pip /usr/bin/pip-python2.7 \
    # 配置默认为python3
    && ln -s /usr/local/python3/bin/python3.8 /usr/bin/python \
    && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
# 修复因修改python版本导致yum失效问题
RUN set -ex \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/bin/yum \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/libexec/urlgrabber-ext-down \
    && yum install -y deltarpm
# 基础环境配置
RUN set -ex \
    # 修改系统时区为东八区
    && rm -rf /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && yum install -y vim \
    # 安装定时任务组件
    && yum -y install cronie
# 支持中文
RUN yum install kde-l10n-Chinese -y
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
# 更新pip版本
RUN pip install --upgrade pip
ENV LC_ALL zh_CN.UTF-8
# 安装Oracle-python
RUN set -ex \
    # 安装Oracle-client
    && yum install libaio -y \
    && wget http://192.168.121.244/oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm \
    && rpm -ivh oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm \
    && rm -rf oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm \
    && cd /usr/lib/oracle/11.2/client64/lib \
    && ln -s libclntsh.so.11.1 libclntsh.so \
    && ln -s libocci.so.11.1 libocci.so \
    && sh -c "echo /usr/lib/oracle/11.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf" \
    && echo "export LD_LIBRARY_PATH=/usr/lib/oracle/11.2/client64/lib:$LD_LIBRARY_PATH" >> /etc/profile \
    && echo "export NLS_LANG=american_america.AL32UTF8" >> /etc/profile \
    && ldconfig \
    && pip install cx_Oracle \
    # 安装prometheus_client
    && pip install prometheus_client

CMD ["python", "/home/docker/oracle.py"]

