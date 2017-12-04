# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import socket
import os
import json
import click
import configparser
from kafka import KafkaConsumer, KafkaProducer
from service_executor import ServiceExecutor
from client_service.shell_service import ShellService


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('SERVICE_NAME')
@click.option('-i', '--interval',  help='Monitor interval millisecond',required=True,type=long)
@click.option('-c', '--coordAddress', help='Coordinate Address')
@click.option('-u', '--user', help='User')
@click.option('-p', '--project_home', help='project home path',required=True)
@click.option('--config', help='config path',required=True)

def monitor(service_name,project_home,interval,coordaddress,user,config):
    print('project_home: {}'.format(project_home))
    print('service_name: {}'.format(service_name))
    print('interval: {}'.format(interval))
    print('coordAddress: {}'.format(coordaddress))
    print('user: {}'.format(user))
    # date convert
    interval_sec = interval/1000

    conf = configparser.ConfigParser()
    conf.read(config)

    supervisor = Supervisor(conf)
    supervisor.execute(service_name,project_home,interval_sec,coordaddress,user)
    

    
class Supervisor(object):
    
    def __init__(self, config):
        # kafka
        self.pub_topic = config['kafka']['HEALTH_TOPIC']
        self.kafka_host = config['kafka']['KAFKA_HOST']
        print('kafka_host: {}'.format(self.kafka_host))
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_host)
        

    def pub_job_result(self, clientIP, project_home,service_name,monitor_pid,service_pid,exec_time,is_success,error_msg,coordAddress,interval,user):
        pub_obj = {
            'clientIP': clientIP,
            'path': project_home,
            'service_name': service_name,
            'monitor_pid': monitor_pid,
            'service_pid': service_pid,
            'exec_time': exec_time,
            'is_success': is_success,
            'error_msg': error_msg,
            'coordAddress': coordAddress if coordAddress is not None else '',
            'interval': interval,
            'user':user if user is not None else '',
        }
        pub_msg = json.dumps(pub_obj)
        self.producer.send(self.pub_topic, pub_msg)

    def execute(self,service_name,project_home,interval_sec,coord_address,user):
        serviceExecutor = ServiceExecutor()
        while True:
            # wait interval seconds
            time.sleep(interval_sec)
            service_pid=''
            error_msg=''
            run_service_cmd = ''
            check_service=serviceExecutor.status_service(service_name)
            # restart
            if (check_service.status!=0):
                print('restart service...')
                restart_service=serviceExecutor.restart_service(service_name)
                print('restart stdout:{}'.format(restart_service.stdout))
                print('restart status:{}'.format(restart_service.status))
                
                if (restart_service.status!=0):
                    is_success=0
                    error_msg=restart_service.stderr
                    error_msg+=restart_service.stdout
                else:
                    is_success=1
                    dobule_check_service=serviceExecutor.status_service(service_name)
                    service_pid = int(dobule_check_service.stdout.split(':')[-1].strip())
            else:
                is_success=1
                # parse pid ,e.g. hippos.service.test1 is running : 8880
                service_pid = int(check_service.stdout.split(':')[-1].strip())
            
            # send message to kafka
            own_pid = os.getpid()
            path = project_home
            exec_time = int(time.time()) * 1000
            ipaddr = socket.gethostbyname(socket.gethostname())

            self.pub_job_result(ipaddr, project_home,service_name,own_pid,service_pid,exec_time,is_success,error_msg,coord_address,interval_sec*1000,user)
            

            


if __name__ == '__main__':
    monitor()
