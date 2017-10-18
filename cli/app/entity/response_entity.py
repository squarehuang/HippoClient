
class RegisterResponse(dict):
    def __init__(self, id, coordAddr=None):
        assert id
        super(RegisterResponse, self).__init__({
            'id': id,
            'coordAddr': coordAddr

        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['id'], dict_obj.get('coordAddr'))


class HippoInstance(dict):
    """ Structure for a HippoInstance.

    Fields:
        id (str)
        pid (str)
        interval (int)
        lastUpdateTime (string)
        state (str)
        config (dict)
            host (str)        
            serviceName (str)
            path (str)
            execTime (str)
    """

    def __init__(self, id=None, pid=None, interval=None, lastUpdateTime=None, state=None, host=None, serviceName=None, path=None, execTime=None):
        super(HippoInstance, self).__init__({
            'id': id,
            'pid': pid,
            'interval': interval,
            'lastUpdateTime': lastUpdateTime,
            'state': state,
            'config': {
                'host': host,
                'serviceName': serviceName,
                'path': path,
                'execTime': execTime
            }
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj.get('id'), dict_obj.get('pid'), dict_obj.get('interval'),
                   dict_obj.get('lastUpdateTime'), dict_obj.get(
                       'state'), dict_obj.get(
                       'config').get('host'), dict_obj.get(
                       'config').get('serviceName'), dict_obj.get(
                       'config').get('path'), dict_obj.get(
                       'config').get('execTime'))


class HippoNode(dict):
    """ Structure for a Hippo Node.
    Fields:
        coordAddr 
        snapshotTime 
        instances (list): A list of Hippo instances.
    """

    def __init__(self, coordAddr=None, snapshotTime=None, instances=None):
        super(HippoNode, self).__init__({
            'coordAddr': coordAddr,
            'snapshotTime': snapshotTime,
            'instances': [x if isinstance(x, HippoInstance) else HippoInstance.from_dict(x) for x in instances]
        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['coordAddr'], dict_obj['snapshotTime'], dict_obj['instances'])


class HippoMsg(dict):
    def __init__(self, message):
        super(HippoMsg, self).__init__({
            'message': message
        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['message'])
