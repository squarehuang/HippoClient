# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback

from controller.base_command import Command
from client.hippo_serving_service import HippoServingService
from entity.request_entity import HippoInstanceRequest
from entity.column_enum import CliBeanColumn


class RestartCommand(Command):
    def __init__(self, api_url):
        super(RestartCommand, self).__init__()
        self.hippoServingService = HippoServingService(api_url)

    def verify_args(self, **kwargs):
        interval = kwargs.get(CliBeanColumn.INTERVAL.value)

        if interval != None:
            interval = interval * 1000
            kwargs[CliBeanColumn.INTERVAL.value] = interval

        return kwargs

    def execute(self, **kwargs):
        try:
            inputs = self.verify_args(**kwargs)
            hippo_id = inputs.get(CliBeanColumn.ID.value)
            interval = inputs.get(CliBeanColumn.INTERVAL.value)

            # call http
            request_entity = HippoInstanceRequest(
                id=hippo_id, interval=interval)
            is_success, resp = self.hippoServingService.restart_service(
                request_entity)

            if not is_success:
                raise Exception(resp.get('message'))
            output_dict = self.refactor_result(resp)
            self.output(output_dict)

        except Exception as e:
            self.logger.error('Start {} service failed'.format(hippo_id))
            self.logger.error(e.message)
            self.logger.error(traceback.format_exc())
