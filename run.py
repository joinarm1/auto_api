#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import shutil
import logging
import logging.handlers
import argparse
import glob
from argparse import RawTextHelpFormatter
from framework.HTMLTestRunner import HTMLTestRunner, stdout_redirector
from framework import config
from framework.util import get_scenario

file_path = os.path.dirname(os.path.realpath(__file__))

_testplan = glob.glob(os.path.join(file_path, "testplan", "*.yaml"))
testplan = [os.path.basename(i) for i in _testplan]
parser = argparse.ArgumentParser(description="Api test platform", formatter_class=RawTextHelpFormatter)
parser.add_argument("-t", "--testplan", choices=testplan, help="which testplan do you want to test\n", default="testplan.yaml")
parser.add_argument("-v", "--verbose", help="Specify the verbosity of output. May be specified multiple times for increased verbosity.", action='count')
parser.add_argument("-r", "--rerun", help="re-run fail/error cases based on the given output file", action='store')
args = parser.parse_args()
if args.verbose > 2:
    level=logging.DEBUG
elif args.verbose > 1:
    level=logging.INFO
elif args.verbose:
    level=logging.WARNING
else:
    level=logging.INFO

result_dir = os.path.join(file_path, "results")
if os.path.exists(result_dir):
    shutil.rmtree(result_dir)
os.mkdir(result_dir)

# log_file = os.path.join(file_path, "results", os.path.splitext(os.path.basename(__file__))[0] + ".log")
log_file = os.path.join(file_path, "results", "result.log")

# write log to stdout
logging.basicConfig(level=logging.DEBUG,
                # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                # stream=stdout_redirector,
                # filename=log_file,
                # filemode='w',
                )

# write log to file, every log's size is 2M
filehander = logging.handlers.RotatingFileHandler(log_file,mode='a', maxBytes=1024*1024*5, backupCount=100, encoding="utf-8")
filehander.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
filehander.setFormatter(formatter)
logging.getLogger('').addHandler(filehander)

# write log to result.html
console = logging.StreamHandler(stream=stdout_redirector)
console.setLevel(level)
formatter = logging.Formatter('%(levelname)-8s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

if not args.testplan:
    parser.print_help()
    logging.error("testplan is not defined!")
    sys.exit(1)

config.testplan = args.testplan
config.rerun = os.path.abspath(args.rerun) if args.rerun else args.rerun

def creatsuite(testplan):
    from scenario.scenario import create_api_scenario_instance
    scenario = get_scenario(testplan)
    suite=unittest.TestSuite()
    for sce in scenario:
        suite.addTests(unittest.makeSuite(create_api_scenario_instance(sce)))
    return suite

def generate_result(title="Auto Test Report"):
    suite = creatsuite(config.testplan)
    result = os.path.join(file_path, "results", "result.html")
    fr = open(result,'wb')
    report = HTMLTestRunner(stream=fr,title=title,verbosity=2)
    res = report.run(suite)
    fr.close()
    return res


if __name__ == '__main__':
    res = generate_result()
    success = int(res.success_count)
    fail = int(res.failure_count)
    error = int(res.error_count)
    all_case = success + fail + error
    print("All: %s, Pass: %s, Fail: %s, Error: %s" % (all_case, success, fail, error))
