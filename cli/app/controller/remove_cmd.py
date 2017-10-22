# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import traceback
from collections import OrderedDict
from base_command import Command
from client_service.hippo_serving_service import HippoServingService
from client_service.hippo_build_service import HippoBuildService
from entity.request_entity import HippoInstanceRequest
from entity.response_entity import HippoInstance
from entity.column_enum import HippoColumn


class RemoveCommand(Command):
    def __init__(self, api_url):
        super(RemoveCommand, self).__init__()
        self.hippoServingService = HippoServingService(api_url)

    def verify_args(self, **kwargs):
        hippo_id = kwargs.get('hippo_id')
        force = kwargs.get('force')
        del_service = kwargs.get('del_service')

        return hippo_id, force, del_service

    def execute(self, **kwargs):
        hippo_id, force, del_service = self.verify_args(**kwargs)
        try:
            request_entity = HippoInstanceRequest(id=hippo_id)
            # stop service
            if force:
                stop_success, stop_resp = self.hippoServingService.stop_service(
                    request_entity)
                if stop_success:
                    print('stop {} success'.format(hippo_id))
            if del_service:
                is_success, status_resp = self.hippoServingService.get_service_status(
                    request_entity)
            # unregister service
            is_success, resp = self.hippoServingService.remove_service(
                request_entity)
            if not is_success:
                raise Exception(resp.get('message'))
            self.output(resp)

            # delete service plugin from project
            if del_service:
                self._execute(status_resp)
        except Exception as e:
            self.logger.error('Remove {} service failed'.format(hippo_id))
            self.logger.error(e.message)
            self.logger.debug(traceback.format_exc)

    def _execute(self, status_resp):
        # 1. get project_home, service name by hippo http
        host = status_resp[HippoColumn.CONFIG.value][HippoColumn.HOST.value]
        project_home = status_resp[HippoColumn.CONFIG.value][HippoColumn.PATH.value]
        service_name = status_resp[HippoColumn.CONFIG.value][HippoColumn.SERVICENAME.value]

        # 2. delete service plugin
        hippo_build_service = HippoBuildService()

        delete_service = hippo_build_service.delete_service(
            service_name=service_name, project_home=project_home, build_server=host)
        if delete_service.status != 0:
            raise Exception("Delete {} Service plugin : {}".format(service_name,
                                                                   delete_service.stderr))
