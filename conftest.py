# import pytest
# from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
#
# # 브라우저 fixture (세션 단위, 한 번만 실행)
# @pytest.fixture(scope="session")
# def browser() -> Browser:
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)  # True/False로 headless 제어
#         yield browser
#         browser.close()
#
#
# # 컨텍스트 fixture (브라우저 환경)
# @pytest.fixture(scope="function")
# def context(browser: Browser) -> BrowserContext:
#     context = browser.new_context()
#
#     # navigator.webdriver 우회
#     context.add_init_script("""
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => undefined
#         });
#     """)
#
#     yield context
#     context.close()
#
#
# # 페이지 fixture
# @pytest.fixture(scope="function")
# def page(context: BrowserContext) -> Page:
#     page = context.new_page()
#     page.set_default_timeout(10000)  # 기본 10초 타임아웃
#     yield page
#     page.close()

import os
import pytest
from playwright.sync_api import sync_playwright

STATE_PATH = "state.json"

@pytest.fixture(scope="session")
def ensure_login_state():
    """로그인 상태가 저장된 state.json을 보장하는 fixture"""
    if not os.path.exists(STATE_PATH):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://www.gmarket.co.kr")
            page.click("text=로그인")
            page.fill("#typeMemberInputId", "cease2504")
            page.fill("#typeMemberInputPassword", "asdf12!@")
            page.click("#btn_memberLogin")

            # state.json 저장
            context.storage_state(path=STATE_PATH)
            browser.close()
    return STATE_PATH


@pytest.fixture(scope="function")
def page(ensure_login_state):
    """로그인 상태가 보장된 페이지 fixture"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=ensure_login_state)
        page = context.new_page()
        yield page
        context.close()
        browser.close()