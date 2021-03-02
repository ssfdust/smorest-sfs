快速开始
====================

首先是如何开始，我自己是用的Archlinux，所以我这里以Archlinux为例，由于这个框架集成了Celery，可能在Windows下的表现有一点问题，不过大体上应该差不多。

准备基础环境
-------------------

1. 安装rabbitmq, redis以及postgres ::

    $ sudo pacman -S redis rabbitmq postgresql

2. 初始化postgresl数据库 ::

    $ sudo -u postgres initdb --locale=en_US.UTF-8 -E UTF8 -D /var/lib/postgres/data

3. 启动服务 ::

    $ sudo systemctl start redis rabbitmq postgreql

4. 新建数据库用户以及开发数据库与测试数据库 ::

    $ sudo -u postgres psql
    postgres=# CREATE USER "smorest-admin" WITH PASSWORD 'smorest2021';
    CREATE ROLE
    postgres=# CREATE DATABASE smorest OWNER "smorest-admin";
    CREATE DATABASE
    postgres=# GRANT ALL PRIVILEGES ON DATABASE smorest TO "smorest-admin";
    GRANT
    postgres=# CREATE DATABASE "smorest-testing" OWNER "smorest-admin";
    CREATE DATABASE
    postgres=# GRANT ALL PRIVILEGES ON DATABASE "smorest-testing" TO "smorest-admin";
    GRANT

准备Python环境
-----------------

1. 准备poetry ::

   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

2. 设置虚拟环境，我这里使用的是pyenv，可以使用其他任意创建虚拟环境的方式代替 ::

    $ pyenv virtualenv 3.8.6 smorest
    Looking in links: /tmp/tmpzrbdmmcj
    Requirement already satisfied: setuptools in /home/ssfdust/.pyenv/versions/3.8.6/envs/smorest/lib/python3.8/site-packages (49.2.1)
    Requirement already satisfied: pip in /home/ssfdust/.pyenv/versions/3.8.6/envs/smorest/lib/python3.8/site-packages (20.2.1)

    $ pyenv local smorest

3. 安装依赖 ::

    $ poetry install

开发准备前
---------------

创建数据表以及写入开发数据 ::

    $ inv app.init.initdb
    $ inv app.init.init-development-data
    请输入初始超级用户密码
    Password:

    $ FLASK_ENV=testing inv app.init.initdb

好了，到这里所有准备工作已经就绪。使用`inv --list`指令来查看支持的指令吧。
