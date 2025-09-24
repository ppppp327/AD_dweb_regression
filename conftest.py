import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

# 브라우저 fixture (세션 단위, 한 번만 실행)
@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # True/False로 headless 제어
        yield browser
        browser.close()


# 컨텍스트 fixture (브라우저 환경)
@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        device_scale_factor=1,
        locale="ko-KR"
    )

    # navigator.webdriver 우회
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

    yield context
    context.close()


# 페이지 fixture
@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    page.set_default_timeout(10000)  # 기본 10초 타임아웃
    yield page
    page.close()