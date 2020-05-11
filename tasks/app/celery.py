"""
Celery相关的Invoke模块
"""
from invoke import task


@task(default=True, help={"level": "日志等级，默认：INFO"})
def start(context, level="INFO"):
    """
    启动Celery服务
    """
    command = f"""
        celery --app=smorest_sfs.app:celery_app worker -l {level} -E -P eventlet
    """
    context.run(command, pty=True)


@task
def beat(context):
    """
    启动Celery Beat服务
    """
    command = f"""
        celery beat -A app.app:celery
        -S app.extensions.mongobeat.schedulers.MongoScheduler
        --pidfile="/tmp/celerybeat.pid"
    """
    context.run(command, pty=True)
