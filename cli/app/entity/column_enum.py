# -*- coding: utf-8 -*-
from enum import Enum


class HippoColumn(Enum):
    __order__ = 'ID SERVICENAME PID INTERVAL STATE HOST PATH LASTUPDATETIME EXECTIME'
    ID = 'id'
    SERVICENAME = 'serviceName'
    PID = 'pid'
    INTERVAL = 'interval'
    STATE = 'state'
    HOST = 'host'
    PATH = 'path'
    LASTUPDATETIME = 'lastUpdateTime'
    EXECTIME = 'execTime'
    CONFIG = 'config'
    COORDADDR = 'coordAddr'


class HippoNodeColumn(Enum):
    __order__ = 'COORDADDR SNAPSHOTTIME INSTANCES'
    COORDADDR = 'coordAddr'
    SNAPSHOTTIME = 'snapshotTime'
    INSTANCES = 'instances'
