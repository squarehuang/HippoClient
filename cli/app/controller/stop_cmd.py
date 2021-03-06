# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import traceback
from collections import OrderedDict
import datetime
import json
from base_command import Command
from client.hippo_serving_service import HippoServingService
from entity.column_enum import HippoColumn, CliBeanColumn
from entity.request_entity import HippoInstanceRequest
from entity.response_entity import HippoInstance


class StopCommand(Command):
    def __init__(self, api_host):
        super(StopCommand, self).__init__()
        self.hippoServingService = HippoServingService(api_host)

    def verify_args(self, **kwargs):
        return kwargs

    def execute(self, **kwargs):
        try:
            inputs = self.verify_args(**kwargs)
            hippo_id = inputs.get(CliBeanColumn.ID.value)
            # call http
            request_entity = HippoInstanceRequest(id=hippo_id)
            is_success, resp = self.hippoServingService.stop_service(
                request_entity)

            if not is_success:
                raise Exception('message: {}\n reason: {}'.format(resp.get('message'),resp.get('reason')))
            output_dict = self.refactor_result(resp)
            self.output(output_dict)

        except Exception as e:
            self.logger.error('Stop {} service failed'.format(hippo_id))
            self.logger.error(e.message)
            self.logger.debug(traceback.format_exc())
