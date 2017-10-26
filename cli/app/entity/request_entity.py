from column_enum import HippoColumn


class HippoInstanceRequest(dict):
    """ Structure for a Request Hippo Instance .

    Fields:
        id (str)
        pid (str)
        interval (int)
        lastUpdateTime (str)
        state (str)
        clientIp (str)        
        serviceName (str)
        path (str)
        execTime (str)
    """

    def __init__(self, id=None, pid=None, interval=None, lastUpdateTime=None, state=None, clientIP=None, serviceName=None, path=None, execTime=None, user=None):
        super(HippoInstanceRequest, self).__init__({
            'id': id,
            'pid': pid,
            'interval': interval,
            'lastUpdateTime': lastUpdateTime,
            'state': state,
            'clientIP': clientIP,
            'serviceName': serviceName,
            'path': path,
            'execTime': execTime,
            'user': user
        })

    def to_simple(self):
        ret = {}
        for col in HippoColumn:
            if self.get(col.value):
                ret[col.value] = self.get(col.value)
        return ret

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj.get('id'), dict_obj.get('pid'), dict_obj.get('interval'),
                   dict_obj.get('lastUpdateTime'), dict_obj.get(
                       'state'), dict_obj.get('clientIP'),
                   dict_obj.get('serviceName'), dict_obj.get('path'), dict_obj.get('execTime'), dict_obj.get('user'))
