# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
topology_lib_python communication library implementation.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division
from __future__ import with_statement


class Shell:
    """
        This class defines a context manager object.

        Usage:

        ::
            with Shell() as ctx:
                ctx.cmd(command)

        This way a Python shell will be opened at the beginning and closed at the end.
        
        """
    def __init__(self, enode, shell=None):
        self.enode = enode
        self.prompt = '>>> '

        if shell is None:
            shell = 'bash'

        self.shell = shell

    def __enter__(self):
        """
        Prepare context opening a python shell
        """
        self.enode.get_shell(self.shell).send_command('python', matches=self.prompt)
        self.enode.get_shell(self.shell).send_command('import sys', matches=self.prompt)
        self.enode.get_shell(self.shell).send_command('sys.path.append("/tmp")', matches=self.prompt)
        return self

    def __exit__(self, type, value, traceback):
        """
        Close python shell
        """
        self.enode.get_shell(self.shell).send_command('exit()')

    
    def cmd(self, command):
        """
        Send instructions to remote python command line
        :param command: instruction to execute remotely
        :type command: string"
        """
        self.enode.get_shell(self.shell).send_command(command, matches=self.prompt)
        response = self.enode.get_shell(self.shell).get_response()
        return response

__all__ = [
    'Shell'
]
