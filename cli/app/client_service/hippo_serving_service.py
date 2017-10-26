# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import traceback
from urllib import urlencode, quote
from collections import OrderedDict
from http_service import HttpService
from entity.column_enum import HippoColumn
from entity.request_entity import HippoInstanceRequest
from entity.response_entity import RegisterResponse, HippoInstance, HippoNode, HippoMsg


class HippoServingService(HttpService):
    """ call serving API. """
    __APP_NAME = 'hippo'
    # __HOST = 'localhost:8080'
    __API_BASE = '/hippo/v0.2.0'

    def __init__(self, host, api_base=None):
        """ Constructor of HippoServing. """
        assert host
        super(HippoServingService, self).__init__(HippoServingService.__APP_NAME,
                                                  api_host=host,
                                                  api_base=api_base if api_base else self.__API_BASE)

    def register_service(self, res):
        """ Register a Service.
        Arguments:
            clientIP
            serviceName
            path
        Return:
            id
        """
        assert res and isinstance(res, HippoInstanceRequest)
        rtn_code, resp = self.request_post(
            '/services', data=res.to_simple())
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))

        if rtn_code == 200 or rtn_code == 201:
            return True, RegisterResponse.from_dict(resp)
        else:
            return False, HippoMsg.from_dict(resp)

    def remove_service(self, res):
        """ Remove a Service.
        Arguments:
            id
        Return:
            message
        """
        assert res
        hippo_id = res['id'] if isinstance(
            res, HippoInstanceRequest) else res

        rtn_code, resp = self.request_delete(
            '/services/instances/{0}'.format(hippo_id))
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))

        if rtn_code == 200:
            return True, HippoMsg.from_dict(resp)
        else:
            return False, HippoMsg.from_dict(resp)

    def start_service(self, res):
        """ Start a Service.
        Arguments:
            id
        Return:
            HippoInstance
        """
        assert res
        hippo_id = res['id'] if isinstance(
            res, HippoInstanceRequest) else res
        rtn_code, resp = self.request_post(
            '/services/instances/{0}/start'.format(hippo_id), data=res.to_simple())
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))

        if rtn_code == 200:
            return True, HippoInstance.from_dict(resp)
        else:
            return False, HippoMsg.from_dict(resp)

    def restart_service(self, res):
        """ Restart a Service.
        Arguments:
            id
        Return:
            HippoInstance
        """
        assert res
        hippo_id = res['id'] if isinstance(
            res, HippoInstanceRequest) else res
        rtn_code, resp = self.request_post(
            '/services/instances/{0}/restart'.format(hippo_id), data=res.to_simple())
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))

        if rtn_code == 200:
            return True, HippoInstance.from_dict(resp)
        else:
            return False, HippoMsg.from_dict(resp)

    def stop_service(self, res):
        """ Stop a Service.
        Arguments:
            id
        Return:
            HippoInstance
        """
        assert res
        hippo_id = res['id'] if isinstance(
            res, HippoInstanceRequest) else res
        rtn_code, resp = self.request_post(
            '/services/instances/{0}/stop'.format(hippo_id), data=res.to_simple())
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))
        if rtn_code == 200:
            return True, HippoInstance.from_dict(resp)
        else:
            return False, HippoMsg.from_dict(resp)

    def get_service_status(self, res):
        """ Get a Service Status.
        Arguments:
            id
        Return:
            HippoInstance
        """
        assert res
        hippo_id = res['id'] if isinstance(
            res, HippoInstanceRequest) else res
        rtn_code, resp = self.request_get(
            '/services/instances/{0}'.format(hippo_id))
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))

        if rtn_code == 200:
            return True, HippoInstance.from_dict(resp)
        else:
            return False, HippoMsg.from_dict(resp)

    def gen_status_querystr(self, res):
        parameters = [HippoColumn.USER.value, HippoColumn.CLIENTIP.value]
        query_str = '?'
        for col in parameters:
            val = res.setdefault(col, None)
            if val is not None:
                query_str += '&{}={}'.format(col, val)
        return query_str

    def get_node_status(self, res):
        """ Get Node Services Status.
        Return:
            HippoInstanceCollection
        """

        query_str = self.gen_status_querystr(res)
        rtn_code, resp = self.request_get(
            '/services/node{}'.format(query_str))
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))
        if rtn_code == 200:
            return True, HippoNode.from_dict(resp)
        else:
            return False, HippoMsg.from_dict(resp)

    def get_cluster_status(self, res):
        """ Get Cluster Services Status.
        Return:
            HippoInstanceCollection
        """
        query_str = self.gen_status_querystr(res)
        rtn_code, resp = self.request_get(
            '/services{}'.format(query_str))
        print(query_str)
        self.logger.debug('rtn_code: {}'.format(rtn_code))
        self.logger.debug('resp: {}'.format(resp))
        if rtn_code == 200:
            return True, [HippoNode.from_dict(node) for node in resp]
        else:
            return False, HippoMsg.from_dict(resp)


def main():
    pass


if __name__ == '__main__':
    main()
