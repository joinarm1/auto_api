import os
import sys
import time
import logging
import json
from requests.exceptions import RequestException

file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(file_dir))

from lib.get_rest import RestClient


class TestBase(object):
    casename = None
    payload = None
    uri = None

    def __init__(self, endpoint='http://dev.aiops.demolx.com/api/', payload={"username":'lxadmin',"password":'Alx0812'}, **args):
        logging.info(args)
        self.args = args
        # self.clt = RestClient('http://127.0.0.1:8080/api/')
        self.clt = RestClient(endpoint)
        self.request("bi/user/login/", method="POST", payload=payload)
        self.setup()

    def setup(self):
        pass

    def run(self):
        raise NotImplementedError()

    @classmethod
    def fetch_all(cls):
        return {s.casename: s for s in cls.__subclasses__()}

    def assert_attr(self, data, key, expect):
        ret = True
        keys = key.split(".") if "." in key else [key]
        for k in keys:
            if k in data:
                actual = data[k]
                data = actual
            else:
                actual = "NOT has this key: %s" % (key)
        try:
            assert str(actual).upper() == str(expect).upper()
        except AssertionError:
            ret = False
        wordmap = {1: "PASS", 0: "FAIL"}
        print(
            "***[{key}] REAL:{real} \n***[{key}] EXPECT:{expect}\n***[{key}] ASSERT:{ret}".format(
                key=key,
                real=actual,
                expect=expect,
                ret=wordmap[ret]))
        return ret

    def assert_has_text(self, output, text):
        ret = text in output
        print("***[ASSERT] %r has text %r : %s" %
              (output, text, {1: "PASS", 0: "FAIL"}[ret]))
        return ret

    def get_attr(self, data, key):
        keys = key.split(".") if "." in key else [key]
        attrval = None
        for k in keys:
            attrval = data[k]
            data = attrval
        return attrval

    def log_result(self, ret, msg="RESULT"):
        print("***%s: %s" % (msg, {1: "SUCCESS", 0: "FAIL"}[ret]))
        return ret

    def log_request(self, uri, method="GET", payload=None):
        print("***[%s] URI:%s PAYLOAD:%s" % (method, uri, payload))

    def request(self, uri, method="GET", payload=None, **kwargs):
        self.log_request(uri, method, payload)

        if method == "POST":
            request_method = self.clt.post
            ret = request_method(uri, json=payload, **kwargs)
        elif method == "PATCH":
            request_method = self.clt.patch
            ret = request_method(uri, json=payload, **kwargs)
        elif method == "DELETE":
            request_method = self.clt.delete
            ret = request_method(uri, json=payload, **kwargs)
        else:
            request_method = self.clt.get
            ret = request_method(uri, params=payload, **kwargs)

        print("[STATUS]:%s" % ret[2])
        print("[RESPONSE]:%s" % json.dumps(ret[1], indent=True, ensure_ascii=False))
        return ret

    def wait(self, sec=10):
        print("*** waiting for %d seconds..." % sec)
        time.sleep(sec)
