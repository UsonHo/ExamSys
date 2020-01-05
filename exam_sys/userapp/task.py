import time
from celery import task
from django.conf import settings


# 删除重置密码的哈希key
@task
def del_resetpwd(key_email):
    time.sleep(5 * 60)
    settings.CONN.hdel(key_email, 'newpwd')
    print('5分钟时间到，redis中链接已失效')
