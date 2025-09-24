from pom.SrpPage import Srp
from pom.VipPage import Vip
from pom.Etc import Etc

#pipenv install pytest-asyncio pytest-xdist
#pipenv run pytest --cache-clear test.py


def test_srp(page):
    etc = Etc(page)
    srp_page = Srp(page)
    vip_page = Vip(page)
    try:
        etc.goto()
        etc.login("cease2504", "asdf12!@")

        srp_page.search_product("무선 이어폰")
        vip_page.select_first_product()
        vip_page.click_buy_now()


    except Exception as e:
        raise e  # 테스트를 실패로 처리
    
def test(page):
    etc = Etc(page)
    srp_page = Srp(page)
    vip_page = Vip(page)
    try:
        etc.goto()
        etc.login("cease2504", "asdf12!@")

        srp_page.search_product("무선 이어폰")
        vip_page.select_first_product()
        vip_page.click_buy_now()


    except Exception as e:
        raise e  # 테스트를 실패로 처리