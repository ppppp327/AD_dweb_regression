from pom.SrpPage import Srp
from pom.Etc import Etc
from utils.db_check import DatabricksSPClient
import time
import json
from utils.TestTimeLogger import TestTimeLogger
import pytest
from search_data import search_testcases1, search_testcases2, search_testcases3, search_testcases4

#pipenv run pytest --cache-clear test.py -s
@pytest.mark.parametrize("keyword, case_id", search_testcases1, ids=[c for _, c in search_testcases1])
def test_srp_1(page, keyword, case_id, request):
    # TestRail 케이스 ID를 현재 실행 노드에 저장
    request.node._testrail_case_id = case_id
    etc = Etc(page)
    srp_page = Srp(page)
    logger = TestTimeLogger("test_srp.json")
    etc.goto()
    etc.login("cease2504", "asdf12!@")

    srp_page.search_product(keyword)
    srp_page.search_module_by_title("먼저 둘러보세요")
    logger.record_time("case1", keyword,"exposure")
    goodscode = srp_page.assert_item_in_module("먼저 둘러보세요")
    logger.record_goodscode("case1",keyword, goodscode)
    logger.record_time("case1", keyword,"click")
    srp_page.montelena_goods_click(goodscode)


#
# def test_srp_2(page):
#     db_check = DatabricksSPClient()
#     time.sleep(902)
#     with open("test_srp.json", "r", encoding="utf-8") as f:
#         test_record = json.load(f)
#     goodscode = test_record[0]["case1"]["상품번호"]
#     click_time = test_record[0]["case1"]["click"]
#     sql = f"select ins_date, cguid from baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt where ins_date >='{click_time}' and item_no ='{goodscode}' and cguid = '11412244806446005562000000' limit 10 ;"
#     a= db_check.query_databricks(sql)
#     print(a)
