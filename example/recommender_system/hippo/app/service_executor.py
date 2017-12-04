# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from client_service.shell_service import ShellService

class ServiceExecutor(ShellService):

    def __init__(self):
        super(ServiceExecutor, self).__init__()

        '''
            check SHELL file path
        '''
        cwd = os.path.dirname(os.path.realpath(__file__))
        app_home = os.path.sep.join(cwd.split(os.path.sep)[:-2])
        paths = [app_home,'hippo', 'bin']
        self.path_prefix = os.path.join(*paths)

    def _merge_options(self, *args, **kwargs):
        options_kv = ['--{0} {1}'.format(k.replace('_', '-'), v)
                      for k, v in kwargs.items() if v != None]

        options_bool = ['--{0}'.format(k) for k in args]
        options_kv.extend(options_bool)
        return ' '.join(options_kv)

   
    def start_service(self, service_name):
        '''
            Usage : run-{servicename}.sh --start
        '''
        assert service_name

        path = os.path.join(self.path_prefix,service_name ,'run-{}.sh'.format(service_name))
        return self.run(
            'bash {0} --start'.format(path))
    
    def restart_service(self, service_name):
        '''
            Usage : run-$servicename.sh --restart
        '''
        assert service_name

        path = os.path.join(self.path_prefix,service_name ,'run-{}.sh'.format(service_name))
        return self.run(
            'bash {0} --restart'.format(path))

    def stop_service(self, service_name):
        '''
            Usage : run-$servicename.sh --stop
        '''
        assert service_name

        path = os.path.join(self.path_prefix,service_name ,'run-{}.sh'.format(service_name))
        return self.run(
            'bash {0} --stop'.format(path))


    def status_service(self, service_name):
        '''
            Usage : run-$servicename.sh --status
        '''
        assert service_name

        path = os.path.join(self.path_prefix,service_name ,'run-{}.sh'.format(service_name))
        return self.run(
            'bash {0} --status'.format(path))
