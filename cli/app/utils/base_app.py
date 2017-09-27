# -*- coding: utf-8 -*-

import logging


class BaseApp(object):

    def __init__(self):
        self._logger = get_logger()

    @property
    def logger(self):
        """ Get logger """
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger


def get_logger(level=logging.INFO):
    logger = logging.getLogger('Hippo CLI')
    logger.setLevel(level)
    if not len(logger.handlers):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(module)s:%(lineno)d - %(message)s'))
        logger.addHandler(ch)

    return logger
