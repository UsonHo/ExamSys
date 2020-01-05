# coding=utf-8
class CtuRequest:
    def __init__(self, event_code, flag, data):
        self.eventCode = event_code
        self.flag = flag
        self.data = data

    def get_event_code(self):
        return self.eventCode

    def get_event_flag(self):
        return self.flag

    def get_data(self):
        return self.data
