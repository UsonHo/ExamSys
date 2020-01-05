# coding=utf-8
class CaptchaResponse:
    result = False
    serverStatus = ""
    def __init__(self, result, serverStatus):
        self.result = result
        self.serverStatus = serverStatus

    def setResult(self, result):
        self.result = result

    def setServerStatus(self, serverStatus):
        self.serverStatus = serverStatus