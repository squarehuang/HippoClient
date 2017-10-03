# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback
import json
import datetime
from base_command import Command
from client_service.hippo_serving_service import HippoServingService
from entity.column_enum import HippoColumn, HippoNodeColumn
from entity.request_entity import HippoInstanceRequest
from entity.response_entity import HippoInstance


class StatusCommand(Command):
    def __init__(self):
        self.hippoServingService = HippoServingService()

    def verify_args(self, **kwargs):
        hippo_id = kwargs.get('hippo_id')
        return hippo_id

    def execute(self, **kwargs):
        hippo_id = self.verify_args(**kwargs)
        try:
            # call http
            request_entity = HippoInstanceRequest(
                id=hippo_id)
            is_success, resp = self.hippoServingService.get_service_status(
                request_entity)

            if not is_success:
                raise Exception(resp.get('message'))
            output_dict = self.refactor_result(resp)
            self.output(output_dict)

        except Exception as e:
            print('Get {} service status failed'.format(hippo_id))
            print(e.message)
            traceback.print_exc()

    def execute_node(self, **kwargs):
        hippo_id = self.verify_args(**kwargs)
        try:
            # call http
            is_success, resp = self.hippoServingService.get_node_status()

            if not is_success:
                raise Exception(resp.get('message'))

            output_dict = self.refactor_node_result(resp)
            oeder_dict = self.output(output_dict)
        except Exception as e:
            print('Get Node status failed')
            print(e.message)
            traceback.print_exc()

    def execute_cluster(self, **kwargs):
        hippo_id = self.verify_args(**kwargs)
        try:
            # call http
            is_success, resp = self.hippoServingService.get_cluster_status()

            if not is_success:
                raise Exception(resp.get('message'))

            output_dict = self.refactor_cluster_result(resp)
            oeder_dict = self.output(output_dict)
        except Exception as e:
            print('Get Node status failed')
            print(e.message)
            traceback.print_exc()

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
