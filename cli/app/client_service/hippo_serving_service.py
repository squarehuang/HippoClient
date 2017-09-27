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
    def __init__(self, hippo_id):
        assert hippo_id
        super(RegisterResponse, self).__init__({
            'hippo_id': hippo_id

        })

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['hippo_id'])


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
        hippo_id (str)
        host (str)
        serviceName (str)
        path (str)
        pid (str)
        state (str)
        checkInterval (int)
        created (str)
        updated (str)
    """

    def __init__(self, hippo_id=None, host=None, serviceName=None, path=None,
                 pid=None, checkInterval=None, state=None, created=None, updated=None, creator=None):
        super(HippoInstance, self).__init__({
            'hippo_id': hippo_id,
            'host': host,
            'serviceName': serviceName,
            'path': path,
            'pid': pid,
            'checkInterval': checkInterval,
            'state': state,
            'created': created,
            'updated': updated,
            'creator': creator
        })

    def to_simple(self):
        ret = {}
        if self.get('hippo_id'):
            ret['hippo_id'] = self.get('hippo_id')
        if self.get('host'):
            ret['host'] = self.get('host')
        if self.get('hippo_id'):
            ret['hippo_id'] = self.get('hippo_id')
        if self.get('serviceName'):
            ret['serviceName'] = self.get('serviceName')
        if self.get('path'):
            ret['path'] = self.get('path')
        if self.get('pid'):
            ret['pid'] = self.get('pid')
        if self.get('checkInterval'):
            ret['checkInterval'] = self.get('checkInterval')
        if self.get('state'):
            ret['state'] = self.get('state')
        if self.get('created'):
            ret['created'] = self.get('created')
        if self.get('state'):
            ret['updated'] = self.get('updated')
        if self.get('creator'):
            ret['creator'] = self.get('creator')
        return ret

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj.get('hippo_id'), dict_obj.get('host'), dict_obj.get('serviceName'),
                   dict_obj.get('path'), dict_obj.get(
                       'pid'), dict_obj.get(
                       'checkInterval'), dict_obj.get(
                       'state'), dict_obj.get(
                       'created'), dict_obj.get(
                       'updated'), dict_obj.get(
                       'creator'))


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
            hippo_id
        """
        assert register_res and isinstance(register_res, RegisterRequest)
        rtn_code, resp = self.request_post(
            '/services', data=register_res.to_simple())
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))

        if rtn_code == 200 or 201:
            return True, RegisterResponse.from_dict(resp)
        else:
            return False, HippoError.from_dict(resp)


def main():
    pass


if __name__ == '__main__':
    main()
