# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import shlex
import subprocess
from client_service.shell_service import ShellService


class HippoBuildService(ShellService):

    def __init__(self):
        super(HippoBuildService, self).__init__()

        '''
            check SHELL file path
        '''
        cwd = os.path.dirname(os.path.realpath(__file__))
        app_home = os.path.sep.join(cwd.split(os.path.sep)[:-4])
        paths = [app_home, 'src', 'plugin']
        self.path_prefix = os.path.join(*paths)

    def _merge_options(self, *args, **kwargs):
        options_kv = ['--{0} {1}'.format(k.replace('_', '-'), v)
                      for k, v in kwargs.items() if v != None]

        options_bool = ['--{0}'.format(k) for k in args]
        options_kv.extend(options_bool)
        return ' '.join(options_kv)

    def install_plugin(self, project_home):
        '''
            Install plugin to Project
            Usage : plugin-installer.sh --install $project_home
        '''
        assert project_home
        path = os.path.join(self.path_prefix, 'plugin-installer.sh')

        return self.run(
            'sh {0} --install {1}'.format(path, project_home))

    def uninstall_plugin(self, instance_id=None, client_ip=None, service_name=None, project_home=None, delete=False, force=False):
        '''
            Uninstall plugin to Project
            Usage : plugin-installer.sh --uninstall $project_home
        '''
        path = os.path.join(self.path_prefix, 'plugin-installer.sh')
        options_bool = []
        if delete:
            options_bool.append('delete')
        if force:
            options_bool.append('force')

        options_str = self._merge_options(*options_bool,
            instance_id=instance_id, client_ip=client_ip, 
            service_name=service_name, project_home=project_home)
        return self.run(
            'bash {0} {1} --uninstall'.format(path, options_str))

    def create_service(self, service_name, project_home, cmd=None):
        '''
            Usage : plugin-installer.sh --create-service=SERVICE $project_home
        '''
        assert service_name
        assert project_home

        path = os.path.join(self.path_prefix, 'plugin-installer.sh')
        options_str = self._merge_options(cmd=cmd)
        self.logger.info('options : {}'.format(options_str))
        return self.run(
            'bash {0} {1} --create-service {2} {3}'.format(path,
                                                           options_str, service_name, project_home))

    def delete_service(self, service_name, project_home):
        '''
            Usage : plugin-installer.sh --delete-service=SERVICE $project_home
        '''
        assert service_name
        assert project_home

        path = os.path.join(self.path_prefix, 'plugin-installer.sh')
        
        return self.run(
            'bash {0} --delete-service {1} {2}'.format(path, service_name, project_home))

    def check_service(self, service_name, project_home):
        '''
            Usage : plugin-installer.sh --check-service=SERVICE $project_home
        '''
        assert service_name
        assert project_home
        path = os.path.join(self.path_prefix, 'plugin-installer.sh')
        return self.run(
            'bash {0} --check-service {1} {2}'.format(path, service_name, project_home))
