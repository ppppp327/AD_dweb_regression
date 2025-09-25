from playwright.sync_api import Page, expect


class Srp():
    def __init__(self, page):
        self.page = page

    def search_product(self, keyword: str):
        """
        홈화면에서 특정 keyword로 검색
        :param (str) keyword : 검색어
        :example:
        """
        runtext = f'Home > {keyword}검색'
        print("#", runtext, "시작")
        self.page.fill("input[name='keyword']", keyword)
        self.page.press("input[name='keyword']", "Enter")
        print("#", runtext, "종료")

    def search_module_by_title(self, module_title):
        """
        특정 모듈의 타이틀 텍스트를 통해 해당 모듈 노출 확인하고 그 모듈 엘리먼트를 반환
        :param (str) module_title : 모듈 타이틀
        :return: 해당 모듈 element
        :example:
        """
        runtext = f'SRP > {module_title}모듈 노출 확인'
        print("#", runtext, "시작")
        child = self.page.get_by_text(module_title)
        child.scroll_into_view_if_needed()
        parent = child.locator("xpath=../..")
        expect(parent).to_be_visible()
        print("#", runtext, "종료")

        return parent


    def assert_item_in_module(self, element):
        child = self.page.get_by_text("먼저 둘러보세요")
        parent = child.locator("xpath=../..")
        expect(parent).to_be_visible()