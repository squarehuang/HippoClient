# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from collections import OrderedDict
import datetime
import json
from base_command import Command
from client_service.hippo_serving_service import HippoServingService, StopRequest, HippoInstance
from entity.response.hippo_status import HippoStatus


class StopCommand(Command):
    def __init__(self):
        self.hippoServingService = HippoServingService()

    def verify_args(self, **kwargs):
        hippo_id = kwargs.get('hippo_id')
        return hippo_id

    def execute(self, **kwargs):
        hippo_id = self.verify_args(**kwargs)
        try:
            # call http
            request_entity = StopRequest(hippo_id)
            is_success, resp = self.hippoServingService.stop_service(
                request_entity)

            if not is_success:
                raise Exception(resp.get('message'))
            output_dict = self.refactor_result(resp)
            output_dict = self.output(output_dict, HippoStatus)

        except Exception as e:
            print('Stop {} service failed'.format(hippo_id))
            print(e.message)

    def refactor_result(self, resp):
        '''
            exectime : timestamp to YYYY-MM-DD HH:mm:ss
            lastupdatetime : timestamp to YYYY-MM-DD HH:mm:ss
            interval : ms to sec 
        '''
        output_dict = {}
        for k, v in resp.items():
            if k == HippoStatus.CONFIG.value:
                for conf_k, conf_v in v.items():
                    if conf_k == HippoStatus.EXECTIME.value:
                        conf_v = datetime.datetime.fromtimestamp(
                            conf_v / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
                    output_dict.setdefault(conf_k, conf_v)
            else:
                if k == HippoStatus.LASTUPDATETIME.value:
                    v = datetime.datetime.fromtimestamp(
                        v / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
                elif k == HippoStatus.INTERVAL.value:
                    v = v / 1000
                output_dict.setdefault(k, v)
        return output_dict
