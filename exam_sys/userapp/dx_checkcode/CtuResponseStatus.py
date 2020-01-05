# coding=utf-8

class CtuResponseStatus:
    SUCCESS = "成功"
    INVALID_REQUEST_PARAMS = "请求不合法,缺少必须参数"
    INVALID_REQUEST_BODY = "请求不合法,请求body为空"
    INVALID_REQUEST_NO_EVENT_DATA = "请求不合法,请求事件的数据为空"
    INVALID_REQUEST_SIGN = "请求签名错误"
    INVALID_APP_KEY = "不合法的appKey"
    INVALID_EVENT_CODE = "不合法的事件"
    INVALID_APP_EVENT_RELATION = "应用和事件的绑定关系错误"

    EVENT_GRAY_SCALE = "事件有灰度控制,非灰度请求"
    NO_POLICY_FOUND = "没有找到防控策略"
    POLICY_HAS_ERROR = "防控策略配置有错误"
    NOT_SUPPORTED_POLICY_OPERATOR = "不支持防控策略里的操作符"

    QPS_EXCEEDING_MAXIMUM_THRESHOLD = "QPS超过最大阀值"

    SERVICE_INTERNAL_ERROR = "服务器内部错误"
    SERVICE_CONNECT_ERROR = "服务器连接错误"
