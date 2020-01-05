# coding=utf-8
import urllib.request, hashlib, json
from .CaptchaResponse import CaptchaResponse


class CaptchaClient:
    requestUrl = "https://cap.dingxiang-inc.com/api/tokenVerify"

    timeout = 2
    response = None

    def __init__(self, appId, appSecret):
        self.appId = appId
        self.appSecret = appSecret

    def setTimeOut(self, timeOut):
        self.timeout = timeOut

    def setCaptchaUrl(self, url):
        self.requestUrl = url

    def checkToken(self, token):
        captchaResponse = CaptchaResponse(False, "")
        # print("token:", token)
        if (self.appId == "" or (self.appId is None) or self.appSecret == ""
            or (self.appSecret is None) or token == "" or (token is None)
            or len(token) > 1024):
            captchaResponse.setServerStatus("参数错误")
            return captchaResponse.__dict__

        arr = token.split(":")

        constId = ""
        if len(arr) == 2:
            constId = arr[1]

        sign = hashlib.md5((self.appSecret + arr[0] + self.appSecret).encode('utf-8')).hexdigest()
        req_url = self.requestUrl + '?appKey=' + self.appId + '&token=' + arr[0] + '&constId=' + constId + "&sign=" + sign

        try:
            self.response = urllib.request.urlopen(req_url, timeout=self.timeout)
            if self.response.code == 200:
                result = self.response.read()
                result = json.loads(result)
                captchaResponse.setServerStatus("SERVER_SUCCESS")
                captchaResponse.setResult(result["success"])
            else:
                captchaResponse.setResult(True)
                captchaResponse.setServerStatus("server error: status=" + str(self.response.code))
            return captchaResponse.__dict__
        except Exception as e:
            captchaResponse.setResult(True)
            captchaResponse.setServerStatus("server error:" + e.message)
            return captchaResponse.__dict__
        finally:
            self.close(self.response)

    def close(self, response):
        try:
            if response != None:
                response.close()
                del response
        except Exception as e:
            print("close response error:" + e.message)
