#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import time
import os
import logging


class GetSSH(paramiko.SSHClient):
    def __init__(self, ip, user, passwd=None, port=22, retry=3, retry_interval=10):
        super(GetSSH, self).__init__()
        self.ip = ip.split(":")[0]
        self.user = user
        self.passwd = passwd
        self.port = port
        self.retry = retry
        self.retry_interval = retry_interval
        self._connect_ssh_server(self.ip, self.user, self.passwd, self.port, self.retry, self.retry_interval)

    def _connect_ssh_server(self, ip, user, passwd=None, port=22, retry=3, retry_interval=10):
        if retry < 0:
            raise Exception("No More Retry! Throw Error!")
        private_key = paramiko.RSAKey.from_private_key_file(os.path.join(os.path.expanduser("~"), '.ssh/id_rsa'))
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.connect(ip, port, user, passwd ) if passwd else \
            self.connect(ip, port, user, pkey=private_key)
        except paramiko.ssh_exception.NoValidConnectionsError:
            time.sleep(retry_interval)
            return self._connect_ssh_server(ip, user, passwd, port, retry - 1, retry_interval)
        return self

    def run(self, cmd, root=False, retries = 3, except_rtcode = 0):
        retry = 0
        while(retry < retries):
            retry += 1
            stdin, stdout, stderr = self.exec_command(cmd, get_pty=True)
            print("***[RUN CMD] count %s: %s" % (str(retry),cmd))
            if root:
                stdin.write(self.passwd + '\n')
                stdin.flush()
            line = stdout.readline()
            ret = []
            while line:
                logging.info(line)
                ret.append(line)
                line = stdout.readline()
            returncode = stdout.channel.recv_exit_status()
            print(returncode)
            print("".join(ret))
            if except_rtcode == returncode:
                break
        return returncode, "".join(ret)
