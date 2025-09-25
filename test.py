from pom.SrpPage import Srp
from pom.VipPage import Vip
from pom.Etc import Etc
from utils.db_check import DatabricksSPClient

#pipenv install pytest-asyncio pytest-xdist
#pipenv run pytest --cache-clear test.py


def test_srp_1(page):
    etc = Etc(page)
    srp_page = Srp(page)
    vip_page = Vip(page)
    db_check = DatabricksSPClient()
    etc.goto()
    etc.login("cease2504", "asdf12!@")

    srp_page.search_product("무선 이어폰")
    srp_page.search_module_by_title("먼저 둘러보세요")
    goodscode = srp_page.assert_item_in_module("먼저 둘러보세요")
    srp_page.montelena_goods_click(goodscode)

    sql = "select 'aiclk',dt,cguid,* from baikali1xs.ad_ats_silver.ub_ra_click_gmkt where dt >='20250922' and item_no ='4534737778' limit 10 ;"

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