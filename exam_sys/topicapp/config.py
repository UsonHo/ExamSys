TEMPLATE_EXIST_ERROR = 1001
TOPICNAME_EXIST_ERROR = 1002
TOPICFORMAT_ERROR = 1003

TOPICPARSE_ERROR = 1004
FILLBANKCOL_ERROR = 1005
CHOICECOL_ERROR = 1006
TOPICTOOBIG_ERROR = 1007

USERID_ERROR = 2001
TOPICTYPE_ERROR = 2002
SETTIME_ERROR = 2003
ENDTIME_ERROR = 2004
MATCHNAME_ERROR = 2005
MULTIPLE_ERROR = 2006

DBNOTEXIST_ERROR = 3001


def choicerror(line):
    ChoiceInvalid = ('第%d行选择题格式设置有误' % line, CHOICECOL_ERROR)
    return ChoiceInvalid


def fillbankerror(line):
    FillBankInvalid = ('第%d行填空题格式设置有误' % line, FILLBANKCOL_ERROR)
    return FillBankInvalid


def topicerror():
    TopicInvalid = ('题库解析出错了', TOPICPARSE_ERROR)
    return TopicInvalid

def qsizetoobig():
    QsizeInvalid = ('题库数量太多', TOPICTOOBIG_ERROR)
    return QsizeInvalid
