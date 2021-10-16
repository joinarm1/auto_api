#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import logging
from framework.util import *
from framework import config


#class Scenario(unittest.TestCase):
#    @parameterized.expand(get_case(config.testplan, config.scenario), testcase_func_name=custom_name_func)
#    def test_case(self, name, script, function, parameter, returncode, description):
#        logging.info("*********************************************")
#        logging.info("case name:%s, script:%s, function:%s, parameter:%s, return:%s" %
#            (name, script, function, parameter, returncode))
#        logging.info("Case description: %s" %(description))
#        logging.info("*********************************************")
#        assert run_case(name, script, function, parameter, returncode)

def create_api_scenario_instance(scenario):
    class scenario_instance(unittest.TestCase):
        @parameterized.expand(get_case_v2(config.testplan, scenario), testcase_func_name=custom_name_func)
        def test_case(self, module, casename, parameter, returncode, *args, **kwargs):
            logging.info("=============================================")
            logging.info("module:%s, case name:%s, parameter:%s, return:%s" %
               (module, casename, parameter, returncode))
            logging.info("=============================================")
            assert run_case_v2(module, casename, parameter, returncode, *args, **kwargs)
            
    scenario_instance.__name__ = scenario
    return scenario_instance
