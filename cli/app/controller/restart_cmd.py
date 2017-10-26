# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback

from controller.base_command import Command
from client_service.hippo_serving_service import HippoServingService
from entity.request_entity import HippoInstanceRequest


class RestartCommand(Command):
    def __init__(self, api_url):
        super(RestartCommand, self).__init__()
        self.hippoServingService = HippoServingService(api_url)

    def verify_args(self, **kwargs):
        hippo_id = kwargs.get('hippo_id')
        interval = kwargs.get('interval')

        # sec => ms
        if interval != None:
            interval = interval * 1000

        return hippo_id, interval

    def execute(self, **kwargs):
        hippo_id, interval = self.verify_args(**kwargs)
        try:
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
