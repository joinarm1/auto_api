# -*- coding: utf-8 -*-
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urljoin


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RestClient(requests.Session):

    def __init__(self, endpoint):
        requests.Session.__init__(self)
        self.endpoint = endpoint
        self.response = None

    def get_full_url(self, uri):
        return urljoin(self.endpoint, uri)

    def handle_response(self, resp):
        self.response = resp
        status = resp.status_code
        method = resp.request.method
        rtime = resp.elapsed.total_seconds()
        if method == 'GET':
            success = status in {200} and len(str(resp.content).strip()) > 0
        elif method in {'POST', "PATCH"}:
            success = status in range(200, 207)
        elif method == 'DELETE':
            success = status in {204}
        try:
            data = resp.json()
        except Exception:
            data = resp.content
            print("failed to get JSON on %s" % resp.url)
        return (success, data, status, rtime)

    def get(self, uri, verify=False, *args, **kwargs):
        resp = super(RestClient, self).get(
            self.get_full_url(uri), verify=False, *args, **kwargs)
        return self.handle_response(resp)

    def post(self, uri, verify=False, *args, **kwargs):
        resp = super(RestClient, self).post(
            self.get_full_url(uri), verify=False, *args, **kwargs)
        return self.handle_response(resp)

    def patch(self, uri, verify=False, *args, **kwargs):
        resp = super(RestClient, self).patch(
            self.get_full_url(uri), verify=False, *args, **kwargs)
        return self.handle_response(resp)

    def delete(self, uri, verify=False, *args, **kwargs):
        resp = super(RestClient, self).delete(
            self.get_full_url(uri), verify=False, *args, **kwargs)
        return self.handle_response(resp)


def main():
    clt = RestClient('http://127.0.0.1:8080/api/')
    ret = clt.post("bi/user/login/",data={"username":'lxadmin',"password":'Alx0812'})
    ret = clt.get("bi/log/patterns/get_alert_conf/?pattern_id=201")
    print(ret)

if __name__ == '__main__':
    main()
