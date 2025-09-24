from playwright.sync_api import Page, expect


class Srp():
    def __init__(self, page):
        self.page = page

    def search_product(self, keyword: str):
        self.page.fill("input[name='keyword']", keyword)
        self.page.press("input[name='keyword']", "Enter")

    def before_search(self):

        child = self.page.get_by_text("먼저 둘러보세요")
        parent = child.locator("xpath=..")
        expect(parent).to_be_visible()

    def before_search_item(self):
        child = self.page.get_by_text("먼저 둘러보세요")
        parent = child.locator("xpath=../..")
        expect(parent).to_be_visible()