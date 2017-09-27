# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from base_command import Command
from client_service.hippo_build_service import HippoBuildService
from client_service.hippo_serving_service import HippoServingService, RegisterRequest


# step1. call build.sh (check create service | create service)
# step2. call coordinate (register)


class RegisterCommand(Command):
    def __init__(self):
        self.hippoBuildService = HippoBuildService()
        self.hippoServingService = HippoServingService()

    def verify_args(self, **kwargs):
        project_home = kwargs.get('project_home')
        service_name = kwargs.get('service_name')
        host = kwargs.get('host')
        run_cmd = kwargs.get('run_cmd', None)

        if service_name is None:
            service_name = os.path.basename(project_home)
        return project_home, service_name, host, run_cmd

    def execute(self, **kwargs):
        project_home, service_name, host, run_cmd = self.verify_args(**kwargs)
        try:
            check_service = self.hippoBuildService.check_service(
                service_name=service_name, project_home=project_home, build_server=host)

            # 若 Project 未裝 plugin ，則先進行安裝
            if check_service.status != 0:
                self.hippoBuildService.create_service(
                    service_name=service_name, project_home=project_home, build_server=host, cmd=run_cmd)
                print("Install {0} Hippo Plugin to {1}:{2} ".format(
                    service_name, host, project_home))

            double_check_service = self.hippoBuildService.check_service(
                service_name=service_name, project_home=project_home, build_server=host)

            if double_check_service.status != 0:
                raise Exception("Service plugin not found : {}".format(
                    double_check_service.stderr))

            # call http
            register_request = RegisterRequest(
                host=host, path=project_home, serviceName=service_name)
            is_success, resp = self.hippoServingService.register_service(
                register_request)

            if not is_success:
                raise Exception(resp.get('message'))
            msg = ['{0} : {1}'.format(k, v) for k, v in resp.items()]
            print('\n'.join(msg))

        except Exception as e:
            print('Register {} service failed'.format(service_name))
            print(e.message)
