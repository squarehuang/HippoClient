# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import traceback
import socket
from termcolor import colored, cprint
from utils import common_util

from base_command import Command

from entity.column_enum import CliBeanColumn

from client.hippo_build_service import HippoBuildService
from client.hippo_serving_service import HippoServingService
from entity.request_entity import HippoInstanceRequest


class RegisterCommand(Command):
    def __init__(self, api_url):
        super(RegisterCommand, self).__init__()
        self.hippoBuildService = HippoBuildService()
        self.hippoServingService = HippoServingService(api_url)

    def verify_args(self, **kwargs):
        project_home = kwargs.get(CliBeanColumn.PROJECT_HOME.value)
        service_name = kwargs.get(CliBeanColumn.SERVICE_NAME.value)
        run_cmd = kwargs.get(CliBeanColumn.RUN_CMD.value)

        if service_name is None:
            service_name = os.path.basename(project_home)
            kwargs[CliBeanColumn.SERVICE_NAME.value] = service_name
        if run_cmd is not None:
            run_cmd = '\"{}\"'.format(run_cmd)
            kwargs[CliBeanColumn.RUN_CMD.value] = run_cmd

        return kwargs

    def set_authkey(self, api_url):
        is_success, sshkey_result = self.hippoServingService.get_sshkey()
        sshkey = sshkey_result['key']
        if not is_success:
            raise Exception(sshkey_result.get('message'))
        # check authorized_keys exists
        auth_file = os.path.expanduser('~/.ssh/authorized_keys')
        if not os.path.exists(auth_file):
            with open(auth_file, 'w'):
                pass
            self.logger.info("create {}".format(auth_file))

        exists_key = list()
        with open(auth_file) as f:
            line = f.readline()
            exists_key.append(line)
        if sshkey not in exists_key:
            self.logger.info(
                "Add hippo manager ({}) ssh key to lcoal".format(api_url))
            self.logger.info(sshkey)
            with open(auth_file, 'a') as f:
                f.write(sshkey)
        self.logger.info('Set Authkey Success')
        print()

    def execute(self, **kwargs):
        inputs = self.verify_args(**kwargs)
        project_home = inputs.get(CliBeanColumn.PROJECT_HOME.value)
        service_name = inputs.get(CliBeanColumn.SERVICE_NAME.value)
        client_ip = inputs.get(CliBeanColumn.CLIENT_IP.value)
        run_cmd = inputs.get(CliBeanColumn.RUN_CMD.value)
        user = inputs.get(CliBeanColumn.USER.value)
        api_url = inputs.get(CliBeanColumn.API_URL.value)

        try:
            check_service = self.hippoBuildService.check_service(
                service_name=service_name, project_home=project_home)

            # 若 Project 未裝 plugin ，則先進行安裝
            if check_service.status != 0:
                create_service = self.hippoBuildService.create_service(
                    service_name=service_name, project_home=project_home,  cmd=run_cmd)
                print("Install {0} Hippo Plugin to {1}:{2} ".format(
                    service_name, client_ip, project_home))
                self.logger.info('==== create service ====')
                self.logger.info(create_service.stdout)

                double_check_service = self.hippoBuildService.check_service(
                    service_name=service_name, project_home=project_home)

                if double_check_service.status != 0:
                    raise Exception("Service plugin not found : {}".format(
                        double_check_service.stderr))
            conf_name = '{}-env.conf'.format(service_name)
            conf_path = os.path.join(
                project_home, 'hippo', 'etc', service_name, conf_name)

            cprint('Please confirm that the {} file is filled in correctly'.format(
                conf_path), 'green')
            cprint('================{} Header ====================='.format(
                conf_name), 'blue')
            common_util.print_by_file(conf_path, 'blue')
            cprint('================{} Footer =====================\n'.format(
                conf_name), 'blue')
            # TODO
            self.set_authkey(api_url)
            # call http
            register_request = HippoInstanceRequest(
                clientIP=client_ip, path=project_home, serviceName=service_name, user=user)
            is_success, resp = self.hippoServingService.register_service(
                register_request)

            if not is_success:
                raise Exception(resp.get('message'))
            self.output(resp)

        except Exception as e:
            self.logger.error(
                'Register {} service failed'.format(service_name))
            self.logger.error(e.message)
            self.logger.error(traceback.format_exc())
