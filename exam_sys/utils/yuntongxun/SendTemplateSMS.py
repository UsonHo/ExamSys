# coding=gbk
# coding=utf-8
# -*- coding: UTF-8 -*-

# 取消证书验证
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

from utils.yuntongxun.CCPRestSDK import REST
import logging
from django.conf import settings
import random
from .config import EXPIRETIME

# 修改_serverIP的值
_serverIP = 'app.cloopen.com'

# import ConfigParser
# 主帐号
accountSid = '8aaf07***'
# 主帐号Token
accountToken = '5012f3****'
# accountToken = 'dc7ca1382621***'
# 应用Id
appId = '8aaf07086f0d2c*****'
# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'
# 请求端口
serverPort = '8883'
# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

class CCPSMS(object):
    def __init__(self, *args, **kwargs):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    # 利用静态方法实现单例模式
    @staticmethod
    def instance():
        if not hasattr(CCPSMS, '_instance'):
            CCPSMS._instance = CCPSMS()
        return CCPSMS._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
            print("状态码：", result, type(result))
        except Exception as e:
            print(e)
            logging.error(e)
            raise e
        if result.get('statusCode') == '000000':
            return True
        else:
            print('请求发送失败')
            return False

    def generatecode(self, phone):
        ''' 4位随机短信验证码'''
        # code = '%04d'%(random.randint(0, 9999))
        # 根据手机号来随机产生6位数字作为验证码
        code = ''
        for i in range(4):
            code += '%s'%random.choice(phone)
        print("短息验证码：", code)
        # 保存到redis数据库中
        settings.CONN.setex('sms%s' % phone, EXPIRETIME, code)
        return code


ccp = CCPSMS.instance()

# ccp = CCPSMS.instance()
# if __name__ == '__main__':
#     ccp = CCPSMS.instance()
#     ccp.sendTemplateSMS("173****", ["短信验证码", "12345"], 1)

'''
def sendTemplateSMS(to,datas,tempId):
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.sendTemplateSMS(to,datas,tempId)
    for k,v in result.iteritems(): 
        
        if k=='templateSMS' :
                for k,s in v.iteritems(): 
                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)
'''
# sendTemplateSMS(手机号码,内容数据,模板Id)
