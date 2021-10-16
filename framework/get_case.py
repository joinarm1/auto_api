#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import re
from pyquery import PyQuery
from framework import config
from parameterized import param


class GetCase(object):
    def __init__(self, testplan):
        self.testplan = testplan

    def load_yml(self, config):
        fr = open(config, "r")
        data = yaml.load(fr, Loader=yaml.FullLoader)
        fr.close()
        return data

    def generate_num(self, num):
        count = 0
        tmp = int(num)
        while tmp != 0:
            tmp = tmp/10
            count +=1
        return count

    def add_zero_func(self, num, count):
        tmp = str(num)
        for i in range(count):
            tmp = "0" + tmp
        return tmp

    def get_case_v2(self, scenario):
        ret = []
        data = self.load_yml(self.testplan)
        sce_arr = [s["module"] for s in data["scenario"]]
        if scenario not in sce_arr:
            return ret
        s_idx = sce_arr.index(scenario)
        sce = data["scenario"][s_idx]
        count = 0
        for c_idx, c in enumerate(sce["cases"]):
            if c.get("skip") is True:
                continue
            count +=1
            one = {
                "module": sce["module"],
                "returncode": True,
                "parameter": {},
            }
            c["casetitle"] = "%02d_%02d_%s" % (s_idx + 1, count, c["casename"])
            one.update(c)
            ret.append(param(**one))
        return ret

    def get_case(self, scenario):
        case_list = []
        data = self.load_yml(self.testplan)
        if data.get("version") not in {"v1", None}:
            return case_list

        if scenario in data.keys():
            max_count = self.generate_num(len(data[scenario]))
            i = 1

            rerun = set(get_failed_cases(config.rerun))
            for case in sorted(data[scenario]):
                if rerun and case not in rerun:
                    continue
                case_count = self.generate_num(i)
                add_zero = int(max_count) - int(case_count)
                case_num = self.add_zero_func(i, add_zero)
                # name, script, function, parameter, returncode, description
                case_list.append(
                    (case_num + "_" + case,
                    data[scenario][case]["script"],
                    data[scenario][case]["function"],
                    data[scenario][case]["parameter"],
                    data[scenario][case].get("returncode", True),
                    data[scenario][case].get("description", None)
                ))
                i += 1
        else:
            return []
        return sorted(case_list)

    def get_all_scenario(self):
        scenario_list = []
        data = self.load_yml(self.testplan)
        for scenario in data.keys():
            scenario_list.append(scenario)
        return scenario_list

    def get_all_scenario_v2(self):
        data = self.load_yml(self.testplan)
        return [s["module"] for s in data["scenario"]]
        
def get_failed_cases(fp):
    ret = []
    if not fp:
        return ret
    with open(fp) as inf:
        html = inf.read()
    q = PyQuery(html)
    pat = re.compile(r"test_case_\d+_(.*)")
    for div_tc in q(".failCase, .errorCase").find("div.testcase"):
        txt = pat.search(PyQuery(div_tc).text()).group(1)
        ret.append(txt)
    return ret

if __name__ == "__main__":
    file_path = os.path.dirname(os.path.realpath(__file__))
    testplan = os.path.join(file_path, "..", "testplan/testplan.yaml")
    getcase = GetCase(testplan)
    print(getcase.get_case("TestBootManager"))
    print(getcase.get_all_scenario())
