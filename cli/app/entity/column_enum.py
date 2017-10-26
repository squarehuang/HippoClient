# -*- coding: utf-8 -*-
from enum import Enum


class HippoColumn(Enum):
    __order__ = 'ID SERVICENAME PID INTERVAL STATE CLIENTIP PATH LASTUPDATETIME EXECTIME USER'
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
    COORDADDR = 'coordAddr'
    USER = 'user'


class HippoNodeColumn(Enum):
    __order__ = 'COORDADDRESS SNAPSHOTTIME INSTANCES'
    COORDADDRESS = 'coordAddress'
    SNAPSHOTTIME = 'snapshotTime'
    INSTANCES = 'instances'
