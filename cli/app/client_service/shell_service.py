# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import shlex
import subprocess
from utils.base_app import BaseApp


class std_output(str):

    @property
    def lines(self):
        return self.split("\n")

    @property
    def qlines(self):
        return [line.split() for line in self.split("\n")]


class ShellService(BaseApp, object):

    def __init__(self):
        pass
        # self.process = None
        # self._status = None
        # self._stdout = None
        # self._stderr = None

    def _create_process(self, command, stdin, cwd, env, shell):
        return subprocess.Popen(
            shlex.split(command),
            universal_newlines=True,
            shell=shell,
            cwd=cwd,
            env=env,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    # @property
    # def status(self):
    #     return self._status

    # @property
    # def stdout(self):
    #     return self._stdout

    # @property
    # def stderr(self):
    #     return self._stderr

    def run(self, cmd, **kwargs):

        env = dict(os.environ)
        env.update(kwargs.get('env', {}))

        cwd = kwargs.get('cwd')
        shell = kwargs.get('shell', False)

        stdin = kwargs.get('stdin', subprocess.PIPE)

        process = self._create_process(
            cmd, stdin, cwd=cwd, env=env, shell=shell)

        stdout, stderr = process.communicate()
        rtncode = process.returncode

        obj = super(ShellService, self).__new__(ShellService, cmd)

        obj.process = process
        obj.pid = process.pid
        obj.command = cmd
        obj.stdout = stdout
        obj.stderr = stderr
        obj.status = rtncode

        return obj
