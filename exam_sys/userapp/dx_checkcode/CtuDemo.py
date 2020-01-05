# coding=utf-8
import json
from .CtuRequest import CtuRequest
from .CtuClient import CtuClient
from .RiskLevel import RiskLevel

class CtuDemo:
    URL = "https://sec.dingxiang-inc.com/ctu/event.do"
    #风控引擎url
    APP_ID = 'appId'
    #应用AppId，公钥
    APP_SECERT = 'appSecret'
    #应用AppSecret，私钥
    if __name__ == '__main__':
        event_code = 'event_code'
        flag = 'test1'
        data = { #业务请求数据，根据实际情况传入
            'const_id': 'constId',
            'user_id': '123',
            'phone_number': '15700000000',
            'ip': '127.0.0.1'
        }
        ctuRequest = CtuRequest(event_code, flag, data)
        client = CtuClient(URL, APP_ID, APP_SECERT)
        #client.timeout = 2
        #设置超时时间 默认两秒
        ctuResponse = client.checkRisk(ctuRequest)
        #向风控引擎发送请求，获取引擎返回的结果
        print(ctuResponse)
        if ctuResponse["result"]["riskLevel"] == RiskLevel.ACCEPT:
            print("当前请求没有风险")
            pass
        elif ctuResponse["result"]["riskLevel"] == RiskLevel.REVIEW:
            print("当前请求有一定风险，建议复审")
            pass
        elif ctuResponse["result"]["riskLevel"] == RiskLevel.REJECT:
            print("当前请求有风险，建议拒绝")
            pass

