# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import traceback
from http_service import HttpService


class RegisterRequest(dict):
    def __init__(self, host, path, serviceName):
        assert host
        assert path
        assert serviceName
        super(RegisterRequest, self).__init__({
            'host': host,
            'path': path,
            'serviceName': serviceName

        })

    def to_simple(self):
        ret = {'host': self['host'], 'path': self['path'],
               'serviceName': self['serviceName']}

        return ret

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['host'], dict_obj['path'], dict_obj['serviceName'])


class RegisterResponse(dict):
    def __init__(self, id):
        assert id
        super(RegisterResponse, self).__init__({
            'id': id

        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['id'])


class StartRequest(dict):
    def __init__(self, id=None, interval=None):
        assert id
        super(StartRequest, self).__init__({
            'id': id,
            'interval': interval
        })

    def to_simple(self):
        ret = {}
        if self.get('interval'):
            ret['interval'] = self.get('interval')
        return ret

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj.get('interval'))


class StopRequest(dict):
    def __init__(self, id=None):
        assert id
        super(StopRequest, self).__init__({
            'id': id
        })

    def to_simple(self):
        ret = {}
        return ret


class HippoError(dict):
    def __init__(self, message):
        super(HippoError, self).__init__({
            'message': message
        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['message'])


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


class HippoInstanceCollection(dict):
    """ Structure for a Hippo Instance.
    Fields:
        HippoInstanceCollection (list): A list of Hippo instances.
    """

    def __init__(self, instanceCollection=None):
        if HippoInstanceCollection is None:
            instanceCollection = []
        assert isinstance(HippoInstanceCollection, list)
        super(HippoInstanceCollection, self).__init__({
            'instanceCollection': [x if isinstance(x, HippoInstance) else HippoInstance.from_dict(x) for x in instanceCollection],
        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['instanceCollection'])


class HippoServingService(HttpService):
    """ call serving API. """
    __APP_NAME = 'hippo'
    __HOST = 'localhost:8080'
    __API_BASE = '/hippo/v0.1.0'

    def __init__(self, host=None, api_base=None):
        """ Constructor of HippoServing. """
        super(HippoServingService, self).__init__(HippoServingService.__APP_NAME,
                                                  api_host=host if host else self.__HOST,
                                                  api_base=api_base if api_base else self.__API_BASE)

    def register_service(self, register_res):
        """ Register a Service.
        Arguments:
            host
            serviceName
            path
        Return:
            id
        """
        assert register_res and isinstance(register_res, RegisterRequest)
        rtn_code, resp = self.request_post(
            '/services', data=register_res.to_simple())
        self.logger.warn('rtn_code: {}'.format(rtn_code))
        self.logger.warn('resp: {}'.format(resp))

        if rtn_code == 200 or 201:
            return True, RegisterResponse.from_dict(resp)
        else:
            return False, HippoError.from_dict(resp)

    def start_service(self, start_res):
        """ Start a Service.
        Arguments:
            id
        Return:
            HippoInstance
        """
        assert start_res
        hippo_id = start_res['id'] if isinstance(
            start_res, StartRequest) else start_res
        rtn_code, resp = self.request_post(
            '/services/instances/{0}/start'.format(hippo_id), data=start_res.to_simple())
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))

        if rtn_code == 200:
            return True, HippoInstance.from_dict(resp)
        else:
            return False, HippoError.from_dict(resp)

    def stop_service(self, stop_res):
        """ Stop a Service.
        Arguments:
            id
        Return:
            HippoInstance
        """
        assert stop_res
        hippo_id = stop_res['id'] if isinstance(
            stop_res, StopRequest) else stop_res
        rtn_code, resp = self.request_post(
            '/services/instances/{0}/stop'.format(hippo_id), data=stop_res.to_simple())
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))
        if rtn_code == 200:
            return True, HippoInstance.from_dict(resp)
        else:
            return False, HippoError.from_dict(resp)


def main():
    pass


if __name__ == '__main__':
    main()
