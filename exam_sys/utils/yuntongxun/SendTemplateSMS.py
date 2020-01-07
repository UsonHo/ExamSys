# coding=gbk
# coding=utf-8
# -*- coding: UTF-8 -*-

# ȡ��֤����֤
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

# �޸�_serverIP��ֵ
_serverIP = 'app.cloopen.com'

# import ConfigParser
# ���ʺ�
accountSid = '8aaf07***'
# ���ʺ�Token
accountToken = '5012f3****'
# accountToken = 'dc7ca1382621***'
# Ӧ��Id
appId = '8aaf07086f0d2c*****'
# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'
# ����˿�
serverPort = '8883'
# REST�汾��
softVersion = '2013-12-26'


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

class CCPSMS(object):
    def __init__(self, *args, **kwargs):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    # ���þ�̬����ʵ�ֵ���ģʽ
    @staticmethod
    def instance():
        if not hasattr(CCPSMS, '_instance'):
            CCPSMS._instance = CCPSMS()
        return CCPSMS._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
            print("״̬�룺", result, type(result))
        except Exception as e:
            print(e)
            logging.error(e)
            raise e
        if result.get('statusCode') == '000000':
            return True
        else:
            print('������ʧ��')
            return False

    def generatecode(self, phone):
        ''' 4λ���������֤��'''
        # code = '%04d'%(random.randint(0, 9999))
        # �����ֻ������������6λ������Ϊ��֤��
        code = ''
        for i in range(4):
            code += '%s'%random.choice(phone)
        print("��Ϣ��֤�룺", code)
        # ���浽redis���ݿ���
        settings.CONN.setex('sms%s' % phone, EXPIRETIME, code)
        return code


ccp = CCPSMS.instance()

# ccp = CCPSMS.instance()
# if __name__ == '__main__':
#     ccp = CCPSMS.instance()
#     ccp.sendTemplateSMS("173****", ["������֤��", "12345"], 1)

'''
def sendTemplateSMS(to,datas,tempId):
    #��ʼ��REST SDK
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
# sendTemplateSMS(�ֻ�����,��������,ģ��Id)
