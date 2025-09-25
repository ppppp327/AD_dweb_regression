from pom.SrpPage import Srp
from pom.VipPage import Vip
from pom.Etc import Etc
from utils.db_check import DatabricksSPClient
from datetime import datetime
import time
import json
from utils.TestTimeLogger import TestTimeLogger
#pipenv run pytest --cache-clear test.py -s


def test_srp_1(page):
    etc = Etc(page)
    srp_page = Srp(page)
    db_check = DatabricksSPClient()
    logger = TestTimeLogger("test_srp.json")
    etc.goto()
    etc.login("cease2504", "asdf12!@")

    srp_page.search_product("무선 이어폰")
    srp_page.search_module_by_title("먼저 둘러보세요")
    logger.record_time("case1", "exposure")
    goodscode = srp_page.assert_item_in_module("먼저 둘러보세요")
    logger.record_time("case1", "click")
    srp_page.montelena_goods_click(goodscode)

    # time.sleep(100)
    #
    # sql = f"select ins_date, cguid from baikali1xs.ad_ats_silver.ub_ad_cpc_click_gmkt where ins_date >='2025-09-25 14:16:00' and item_no ='{goodscode}' limit 10 ;"
    #
    # a= db_check.query_databricks(sql)
    # print(a)



# def test_srp_2(page):
#     etc = Etc(page)
#     srp_page = Srp(page)
#     vip_page = Vip(page)
#     try:
#         etc.goto()
#         etc.login("cease2504", "asdf12!@")
#
#         srp_page.search_product("무선 이어폰")
#         vip_page.select_first_product()
#         vip_page.click_buy_now()
#
#
#     except Exception as e:
#         raise e  # 테스트를 실패로 처리