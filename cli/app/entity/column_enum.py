# -*- coding: utf-8 -*-
from enum import Enum


class CliBeanColumn(Enum):
    ID = 'id'
    PROJECT_HOME = 'project_home'
    SERVICE_NAME = 'service_name'
    CLIENT_IP = 'client_ip'
    RUN_CMD = 'run_cmd'
    API_HOST = 'api_host'
    API_PORT = 'api_port'
    API_URL = 'api_url'
    COORDADDRESS = 'coord_address'
    USER = 'user'
    FORCE = 'force'
    DEL_SERVICE = 'del_service'
    INTERVAL = 'interval'


class HippoColumn(Enum):
    __order__ = 'ID SERVICENAME PID INTERVAL STATE CLIENTIP PATH LASTUPDATETIME EXECTIME COORDADDRESS USER'
    ID = 'id'
    SERVICENAME = 'serviceName'
    PID = 'pid'
    INTERVAL = 'interval'
    STATE = 'state'
    CLIENTIP = 'clientIP'
    PATH = 'path'
    LASTUPDATETIME = 'lastUpdateTime'
    EXECTIME = 'execTime'
    CONFIG = 'config'
    COORDADDRESS = 'coordAddress'
    USER = 'user'


class HippoNodeColumn(Enum):
    __order__ = 'COORDADDRESS SNAPSHOTTIME INSTANCES'
    COORDADDRESS = 'coordAddress'
    SNAPSHOTTIME = 'snapshotTime'
    INSTANCES = 'instances'
