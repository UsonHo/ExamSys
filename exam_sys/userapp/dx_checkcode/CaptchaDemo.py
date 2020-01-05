# coding=utf-8
 # 构造入参为appId和appSecret
 # appId和前端验证码的appId保持一致，appId可公开
 # appSecret为秘钥，请勿公开
 # token在前端完成验证后可以获取到，随业务请求发送到后台，token有效期为两分钟
from .CaptchaClient import CaptchaClient
appId ="appId"
appSecret = "appSecret"

captchaClient = CaptchaClient(appId, appSecret)
captchaClient.setTimeOut(2)
# 设置超时时间，默认2秒
# captchaClient.setCaptchaUrl("http://cap.dingxiang-inc.com/api/tokenVerify")
# 特殊情况可以额外指定服务器，默认情况下不需要设置
response = captchaClient.checkToken("token:")
print(response['serverStatus'])
#确保验证状态是SERVER_SUCCESS，SDK中有容错机制，在网络出现异常的情况会返回通过
print(response['result'])
if response['result']:
    pass
else:
    pass