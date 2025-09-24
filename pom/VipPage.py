class Vip():
    def __init__(self, page):
        self.page = page

    def select_first_product(self):
        self.page.click("css=ul.search-list > li:first-child a")

    def click_buy_now(self):
        self.page.click("text=바로구매")