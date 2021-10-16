#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from framework import config
from framework.get_case import GetCase
from parameterized import parameterized

curdir = os.path.dirname(__file__)
testplandir = os.path.abspath(os.path.join(curdir, "../testplan/"))


def get_parameter(parameter):
    if parameter == "none":
        return config
    else:
        return dict(config, **parameter)

def run_case(name, script, function, parameter, returncode):
    args = get_parameter(parameter)
    logging.debug(args)
    func = __import__('cases.' + script, globals(), locals(), '*')
    logging.debug(func)
    return eval("func.%s"%function)(**args) == returncode

def run_case_v2(module, casename, parameter, returncode, *args, **kwargs):
    args = get_parameter(parameter)
    logging.debug(args)
    mod = __import__('cases.' + module, globals(), locals(), '*')
    logging.debug(mod)
    casemap = getattr(mod, "case_mapping")
    casecls = casemap[casename]
    return casecls(**args).run() == returncode

def custom_name_func(testcase_func, param_num, param):
    return "%s_%s" %(
        testcase_func.__name__,
        parameterized.to_safe_name(param.kwargs.get("casetitle") or param.kwargs["casename"]),
    )

def get_case(testplan, scenario):
    '''
    get case from testplan
    '''
    _testplan = os.path.join(testplandir, testplan)
    getcase = GetCase(_testplan)
    return getcase.get_case(scenario)

def get_case_v2(testplan, scenario):
    _testplan = os.path.join(testplandir, testplan)
    getcase = GetCase(_testplan)
    return getcase.get_case_v2(scenario)
    
def get_scenario(testplan):
    _testplan = os.path.join(testplandir, testplan)
    getcase = GetCase(_testplan)
    filtered = {"version",}
    return [i for i in getcase.get_all_scenario_v2() if i not in filtered]

def get_subclass(cls, sub_classname):
    class sub(cls):
        pass
    sub.__name__ = sub_classname
    return sub