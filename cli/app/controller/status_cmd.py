# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback
import json
import datetime

from base_command import Command
from client.hippo_serving_service import HippoServingService
from entity.column_enum import CliBeanColumn, HippoColumn, HippoNodeColumn

from entity.request_entity import HippoInstanceRequest
from entity.response_entity import HippoInstance


class StatusCommand(Command, object):
    def __init__(self, api_url):
        super(StatusCommand, self).__init__()
        self.hippoServingService = HippoServingService(api_url)

    def verify_args(self, **kwargs):
        return kwargs

    def execute(self, **kwargs):
        inputs = self.verify_args(**kwargs)
        hippo_id = inputs.get(CliBeanColumn.ID.value)
        try:
            # call http
            request_entity = HippoInstanceRequest(
                id=hippo_id)
            is_success, resp = self.hippoServingService.get_service_status(
                request_entity)

            if not is_success:
                raise Exception('message: {}\n reason: {}'.format(resp.get('message'),resp.get('reason')))
            output_dict = self.refactor_result(resp)
            self.output(output_dict)

        except Exception as e:
            self.logger.error('Get {} service status failed'.format(hippo_id))
            self.logger.error(e.message)
            self.logger.debug(traceback.format_exc())

    def execute_node(self, **kwargs):
        try:
            inputs = self.verify_args(**kwargs)
            user = inputs.get(CliBeanColumn.USER.value)
            client_ip = inputs.get(CliBeanColumn.CLIENT_IP.value)

            request_entity = HippoInstanceRequest(
                user=user, clientIP=client_ip)

            # call http
            is_success, resp = self.hippoServingService.get_node_status(
                request_entity)

            if not is_success:
                raise Exception(resp.get('message'))

            output_dict = self.refactor_node_result(resp)
            oeder_dict = self.output(output_dict)
        except Exception as e:
            self.logger.error('Get Node status failed')
            self.logger.error(e.message)
            self.logger.debug(traceback.format_exc())

    def execute_cluster(self, **kwargs):
        try:
            inputs = self.verify_args(**kwargs)
            user = inputs.get(CliBeanColumn.USER.value)
            client_ip = inputs.get(CliBeanColumn.CLIENT_IP.value)

            request_entity = HippoInstanceRequest(
                user=user, clientIP=client_ip)
            # call http
            is_success, resp = self.hippoServingService.get_cluster_status(
                request_entity)

            if not is_success:
                raise Exception(resp.get('message'))

            output_dict = self.refactor_cluster_result(resp)
            oeder_dict = self.output(output_dict)
        except Exception as e:
            self.logger.error('Get Node status failed')
            self.logger.error(e.message)
            self.logger.debug(traceback.format_exc())

    def refactor_cluster_result(self, resp):
        node_list = []
        for node in resp:
            node_info = self.refactor_node_result(node)
            node_list.append(node_info)
        return node_list

    def refactor_node_result(self, resp):
        node_dict = {}
        service_list = []

        for k, v in resp.items():
            if k == HippoNodeColumn.INSTANCES.value:
                for instance in v:
                    service_info = self.refactor_result(instance)
                    service_list.append(service_info)
                v = service_list
            elif k == HippoNodeColumn.SNAPSHOTTIME.value:
                v = datetime.datetime.fromtimestamp(
                    v / 1000.0).strftime("%Y-%m-%d %H:%M:%S")

            node_dict.setdefault(k, v)

        # order
        output_dict_ordered = self.order_dict(node_dict, HippoNodeColumn)
        return output_dict_ordered
