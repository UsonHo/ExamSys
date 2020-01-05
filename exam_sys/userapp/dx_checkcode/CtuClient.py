# coding=utf-8
from .CtuRequest import CtuRequest
from .CtuResponse import CtuResponse
from .CtuResult import CtuResult
from .RiskLevel import RiskLevel
from .CtuResponseStatus import CtuResponseStatus
import json
import hashlib
import requests
import base64
import uuid

class CtuClient:
    version = 1
    timeout = 2
    def __init__(self, url, app_key, app_secret):
        self.url = url
        self.appKey = app_key
        self.appSecret = app_secret
    def setTimeOut(self, timeOut):
        self.timeout = timeOut

    def checkRisk(self, ctu_request):
        if not isinstance(ctu_request, CtuRequest):
            raise Exception('Sign mode must specify typeof CtuRequest')

        sign = self.sign(self.appSecret, ctu_request)

        req_url = self.url + '?appKey=' + self.appKey + '&sign=' + sign + '&version=' + str(self.version)

        request_json_dict = ctu_request.__dict__
        request_json = json.dumps(request_json_dict)
        try:
            response = requests.post(url=req_url, data=base64.b64encode(request_json), timeout=self.timeout)
            if response.status_code != 200:
                ctuResult = CtuResult(RiskLevel.ACCEPT, "")
                ctuResponse = CtuResponse(uuid.uuid1(), CtuResponseStatus.SERVICE_CONNECT_ERROR, ctuResult.__dict__)
                return ctuResponse.__dict__
            return json.loads(response.content)
        except Exception as e:
            ctuResult = CtuResult(RiskLevel.ACCEPT, "")
            ctuResponse = CtuResponse(uuid.uuid1(), e.message, ctuResult.__dict__)
            return ctuResponse.__dict__

    def sign(self, app_secret, ctu_request):
        if not isinstance(ctu_request, CtuRequest):
            raise Exception('Sign mode must specify typeof CtuRequest')

        sort_params = self.sort_params(ctu_request)
        return hashlib.md5(app_secret + sort_params + app_secret).hexdigest()

    @staticmethod
    def sort_params(ctu_request):
        if not isinstance(ctu_request, CtuRequest):
            raise Exception('Sign mode must specify typeof CtuRequest')
        event_code = ctu_request.get_event_code()
        flag = ctu_request.get_event_flag()

        data_map = ctu_request.get_data()
        items = data_map.items()
        items.sort()
        plain_text = "eventCode" + event_code + "flag" + flag
        for (d, x) in items:
            plain_text += d + str(x)

        return plain_text
