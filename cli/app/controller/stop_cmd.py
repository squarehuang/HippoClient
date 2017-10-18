# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from collections import OrderedDict
import datetime
import json
from base_command import Command
from client_service.hippo_serving_service import HippoServingService
from entity.column_enum import HippoColumn
from entity.request_entity import HippoInstanceRequest
from entity.response_entity import HippoInstance


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
            request_entity = HippoInstanceRequest(id=hippo_id)
            is_success, resp = self.hippoServingService.stop_service(
                request_entity)

            if not is_success:
                raise Exception(resp.get('message'))
            output_dict = self.refactor_result(resp)
            self.output(output_dict)

        except Exception as e:
            print('Stop {} service failed'.format(hippo_id))
            print(e.message)
