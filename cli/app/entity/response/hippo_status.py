# -*- coding: utf-8 -*-

from enum import Enum


class HippoStatus(Enum):
    __order__ = 'ID PID INTERVAL LASTUPDATETIME STATE HOST SERVICENAME PATH EXECTIME'
    ID = 'id'
    PID = 'pid'
    INTERVAL = 'interval'
    LASTUPDATETIME = 'lastUpdateTime'
    STATE = 'state'
    HOST = 'host'
    SERVICENAME = 'serviceName'
    PATH = 'path'
    EXECTIME = 'execTime'
    CONFIG = 'config'
