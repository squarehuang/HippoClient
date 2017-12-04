
class RegisterResponse(dict):
    def __init__(self, id, coordAddress=None):
        assert id
        super(RegisterResponse, self).__init__({
            'id': id,
            'coordAddress': coordAddress

        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['id'], dict_obj.get('coordAddress'))


class KeyResponse(dict):
    def __init__(self, key):
        assert key
        super(KeyResponse, self).__init__({
            'key': key
        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['key'])


class HippoInstance(dict):
    """ Structure for a HippoInstance.

    Fields:
        id (str)
        pid (str)
        interval (int)
        lastUpdateTime (string)
        state (str)
        config (dict)
            clientIP (str)        
            serviceName (str)
            path (str)
            execTime (str)
    """

    def __init__(self, id=None, pid=None, interval=None, lastUpdateTime=None, state=None, clientIP=None, serviceName=None, path=None, execTime=None, user=None):
        super(HippoInstance, self).__init__({
            'id': id,
            'pid': pid,
            'interval': interval,
            'lastUpdateTime': lastUpdateTime,
            'state': state,
            'config': {
                'clientIP': clientIP,
                'serviceName': serviceName,
                'path': path,
                'execTime': execTime,
                "user": user
            }
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj.get('id'), dict_obj.get('pid'), dict_obj.get('interval'),
                   dict_obj.get('lastUpdateTime'), dict_obj.get(
                       'state'), dict_obj.get(
                       'config').get('clientIP'), dict_obj.get(
                       'config').get('serviceName'), dict_obj.get(
                       'config').get('path'), dict_obj.get(
                       'config').get('execTime'), dict_obj.get(
                       'config').get('user'))


class HippoNode(dict):
    """ Structure for a Hippo Node.
    Fields:
        coordAddress 
        snapshotTime 
        instances (list): A list of Hippo instances.
    """

    def __init__(self, coordAddress=None, snapshotTime=None, instances=None):
        super(HippoNode, self).__init__({
            'coordAddress': coordAddress,
            'snapshotTime': snapshotTime,
            'instances': [x if isinstance(x, HippoInstance) else HippoInstance.from_dict(x) for x in instances]
        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['coordAddress'], dict_obj['snapshotTime'], dict_obj['instances'])


class HippoMsg(dict):
    def __init__(self, message,reason=None):
        super(HippoMsg, self).__init__({
            'message': message,
            'reason':reason
        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['message'],dict_obj.get('reason'))
