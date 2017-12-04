# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import traceback

import requests
from base_app import BaseApp


class HttpService(BaseApp, object):
    __common_headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Pragma': 'no-cache'
    }

    def __init__(self, app_name, api_host, api_base):
        """ Constructor
        Args:
            app_name (str): The application name
            api_host (str): The host to make API request to
            api_base (str): The API base of the application
        """
        super(HttpService, self).__init__()
        assert app_name
        self._app_name = app_name
        assert api_host
        self._api_host = api_host
        assert api_base
        self._api_base = api_base

    @property
    def app_name(self):
        """ Get application name """
        return self._app_name

    @property
    def api_host(self):
        """ Get API Host """
        return self._api_host

    @api_host.setter
    def host(self, api_host):
        self._logger.info("Set API host (%s)" % api_host)
        self._api_host = api_host

    @property
    def api_base(self):
        """ Get API base"""
        return self._api_base

    def _resolve_api_url(self, api_postfix):
        return 'http://{0}{1}{2}'.format(self._api_host, self._api_base, api_postfix)

    def request_get(self, url, headers=None, data=None):
        return self._request(url, method='get', headers=headers, data=data)

    def request_post(self, url, headers=None, data=None):
        return self._request(url, method='post', headers=headers, data=data)

    def request_delete(self, url, headers=None):
        return self._request(url, method='delete', headers=headers)

    def _request(self, api, method='get', headers=None, data=None):
        url = self._resolve_api_url(api)
        self.logger.info('connect to {}'.format(url))

        if headers == None:
            headers = self.__common_headers.copy()
        try:
            if method == 'get':
                response = requests.get(url, headers=headers, params=data)
            elif method == 'post':
                response = requests.post(
                    url, headers=headers, data=json.dumps(data))
            elif method == 'delete':
                response = requests.delete(
                    url, headers=headers)
        except Exception as e:
            raise Exception('connect to {} failed'.format(url))

        try:
            return response.status_code, json.loads(response.text)
        except ValueError as e:
            print('{} error: Illegal response ({}) from server'.format(
                str(e.message), response.content))
            self.logger.error(
                '{} error: Illegal response ({}) from server'.format(traceback.extract_stack(), response.content))
        except Exception as e:
            raise Exception('connect to {} failed'.format(url))
