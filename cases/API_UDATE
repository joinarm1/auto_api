from cases.test_base import TestBase


class Test1(TestBase):
    casename = "GET_LOG_PATTERN_LIST_WITHOUT_DT"
    """
    Requirement: get log pattern list without date range
    default items per page: 20
    """

    def run(self):
        uri = "bi/log/patterns/"
        _, data, status, _ = self.request(uri)
        print("*** Get Status: REAL:%s EXPECT:%s" % (status, 200))
        print("*** Get Result: %s" % {1: "SUCCESS", 0: "FAIL"}[status == 200])
        total = data['count']
        if total >= 20:
            assert len(data['results']) == 20
        else:
            print("*** Result: total count is %s less then 20" % len(data['results']))
        return True

class Test2(TestBase):
    casename = "GET_LOG_PATTERN_LIST_WITHOUT_DT_CUSTOM_PAGE_200"
    """
    Requirement: get log pattern list without date range
    items per page: 200
    """

    def run(self):
        uri = "bi/log/patterns/"
        _, data, status, _ = self.request(uri, payload={"limit":200, "offset":0})
        print("*** Get Status: REAL:%s EXPECT:%s" % (status, 200))
        print("*** Get Result: %s" % {1: "SUCCESS", 0: "FAIL"}[status == 200])
        total = data['count']
        if total >= 200:
            assert len(data['results']) == 200
        else:
            print("*** Result: total count is %s less then 200" % len(data['results']))
        return True

class Test3(TestBase):
    casename = "GET_LOG_PATTERN_LIST_WITHOUT_DT_CUSTOM_PAGE_500"
    """
    Requirement: get log pattern list without date range
    items per page: 500
    """

    def run(self):
        uri = "bi/log/patterns/"
        _, data, status, _ = self.request(uri, payload={"limit":500, "offset":0})
        print("*** Get Status: REAL:%s EXPECT:%s" % (status, 200))
        print("*** Get Result: %s" % {1: "SUCCESS", 0: "FAIL"}[status == 200])
        total = data['count']
        if total >= 500:
            assert len(data['results']) == 500
        else:
            print("*** Result: total count is %s less then 500" % len(data['results']))
        return True

case_mapping = TestBase.fetch_all()
