#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
import time
import json

curdir = os.path.dirname(__file__)

pro_dir = os.path.join(curdir, "..")

class GetProcess(object):

    def __init__(self):
        pass

    def debug(self, message=""):
        print(message)

    def debug_log(self, tmpfile):
        try:
            with open(tmpfile) as f:
                logging.debug(f.readlines())
        except:
            pass

    def error_log(self, tmpfile):
        try:
            with open(tmpfile) as f:
                logging.error(f.readlines())
        except:
            pass

    def dump_json(self, data, filename, **kwargs):
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)
        save_path = os.path.join(self.log_dir, filename)
        with open(save_path, "w") as outf:
            json.dump(data, outf, **kwargs)

    def log_msg(self, msg):
        roothandlers = logging.root.handlers
        if len(roothandlers) == 0:
            print(msg)
        elif len(roothandlers) == 1:
            if isinstance(roothandlers[0], logging.StreamHandler):
                print(msg)
        logging.info(msg)

    def execute_cmd(self, cmd, retry_max=3, retry_interval=30, on_fail=None):
        """
        `retry` action will be ignored while `on_fail` callback is given
        """
        retry_cnt = 0
        while retry_cnt <= retry_max:
            self.log_msg("run cmd: %s" % cmd)
            p = subprocess.Popen(cmd, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            p.wait()
            if p.returncode != 0:
                if on_fail is not None:
                    return on_fail(p)
                if retry_cnt == retry_max:
                    return p
                retry_cnt += 1
                self.log_msg(">> `return` should be int `0`, wait %s seconds and retry (%s/%s)." % \
                    (retry_interval, retry_cnt, retry_max))
                time.sleep(retry_interval)
            else:
                return p
