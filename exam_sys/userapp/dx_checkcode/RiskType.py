from enum import Enum

class RiskType(Enum):
    RUBBISH_REGISTRATION = "垃圾注册"
    ACCOUNT_STOLEN = "账号盗用"
    MACHINE_CRAWLING = "机器爬取"
    BATCH_LOGON = "批量登陆"
    MALICIOUS_GRAB = "黄牛抢单"
    UNKNWON = "未定义"
