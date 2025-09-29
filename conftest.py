import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from src.gtas_python_core.gtas_python_core_testrail import *
from src.gtas_python_core.gtas_python_core_vault import Vault
import os
import pytest
import requests
from datetime import datetime

# 브라우저 fixture (세션 단위, 한 번만 실행)
@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])  # True/False로 headless 제어
        yield browser
        browser.close()


# 컨텍스트 fixture (브라우저 환경)
@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(no_viewport=True)

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



with open('config.json') as config_file:
    config = json.load(config_file)

# 환경변수 기반 설정
TESTRAIL_BASE_URL = config['tr_url']
TESTRAIL_PROJECT_ID = config['project_id']
TESTRAIL_SUITE_ID = config['suite_id']
TESTRAIL_SECTION_NAME = config['section_name']  # ✅ 섹션 이름으로 지정
TESTRAIL_USER = (Vault("gmarket").get_Kv_credential("authentication/testrail/automation")).get("username")
TESTRAIL_TOKEN = (Vault("gmarket").get_Kv_credential("authentication/testrail/automation")).get("password")

testrail_run_id = None
case_id_map = {}  # {섹션 이름: [케이스ID 리스트]}


def testrail_get(endpoint):
    url = f"{TESTRAIL_BASE_URL}/index.php?/api/v2/{endpoint}"
    r = requests.get(url, auth=(TESTRAIL_USER, TESTRAIL_TOKEN))
    r.raise_for_status()
    return r.json()


def testrail_post(endpoint, payload):
    url = f"{TESTRAIL_BASE_URL}/index.php?/api/v2/{endpoint}"
    r = requests.post(url, json=payload, auth=(TESTRAIL_USER, TESTRAIL_TOKEN))
    r.raise_for_status()
    return r.json()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    테스트 실행 시작 시:
    1. 섹션 이름으로 section_id 찾기
    2. 해당 섹션의 케이스 ID 가져오기
    3. 그 케이스들로 Run 생성
    """
    global testrail_run_id, case_id_map

    # 1. 섹션 목록 불러오기
    sections = testrail_get(f"get_sections/{TESTRAIL_PROJECT_ID}&suite_id={TESTRAIL_SUITE_ID}")
    section_id = None
    for s in sections:
        if s["name"] == TESTRAIL_SECTION_NAME:
            section_id = s["id"]
            break

    if not section_id:
        raise RuntimeError(f"[TestRail] 섹션 '{TESTRAIL_SECTION_NAME}'을(를) 찾을 수 없습니다.")

    # 2. 섹션 내 케이스 가져오기
    cases = testrail_get(
        f"get_cases/{TESTRAIL_PROJECT_ID}&suite_id={TESTRAIL_SUITE_ID}&section_id={section_id}"
    )
    case_ids = [c["id"] for c in cases]
    case_id_map[TESTRAIL_SECTION_NAME] = case_ids

    if not case_ids:
        raise RuntimeError(f"[TestRail] 섹션 '{TESTRAIL_SECTION_NAME}'에 케이스가 없습니다.")

    # 3. Run 생성
    run_name = f"자동화 테스트 실행 ({TESTRAIL_SECTION_NAME}) {datetime.now():%Y-%m-%d %H:%M:%S}"
    payload = {
        "suite_id": TESTRAIL_SUITE_ID,
        "name": run_name,
        "include_all": False,
        "case_ids": case_ids
    }
    run = testrail_post(f"add_run/{TESTRAIL_PROJECT_ID}", payload)
    testrail_run_id = run["id"]

    print(f"[TestRail] 섹션 '{TESTRAIL_SECTION_NAME}' Run 생성 완료 (ID={testrail_run_id})")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    각 테스트 결과를 TestRail에 기록
    """
    outcome = yield
    result = outcome.get_result()

    case_id = getattr(item, "_testrail_case_id", None)
    if case_id is None or testrail_run_id is None:
        return

    if result.when == "call":  # 실행 시점 결과만 기록
        if result.failed:
            status_id = 5  # Failed
            comment = f"테스트 실패: {result.longrepr}"
        elif result.skipped:
            status_id = 2  # Blocked
            comment = "테스트 스킵"
        else:
            status_id = 1  # Passed
            comment = "테스트 성공"

        payload = {"status_id": status_id, "comment": comment}
        testrail_post(f"add_result_for_case/{testrail_run_id}/{case_id}", payload)
        print(f"[TestRail] case {case_id} 결과 기록 ({status_id})")


def pytest_sessionfinish(session, exitstatus):
    """
    전체 테스트 종료 후 Run 닫기
    """
    global testrail_run_id
    if testrail_run_id:
        testrail_post(f"close_run/{testrail_run_id}", {})
        print(f"[TestRail] Run {testrail_run_id} 종료 완료")























# import os
# import pytest
# from playwright.sync_api import sync_playwright
#
# STATE_PATH = "state.json"
#
# @pytest.fixture(scope="session")
# def ensure_login_state():
#     """로그인 상태가 저장된 state.json을 보장하는 fixture"""
#     if not os.path.exists(STATE_PATH):
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=False)
#             context = browser.new_context()
#             page = context.new_page()
#
#             page.goto("https://www.gmarket.co.kr")
#             page.click("text=로그인")
#             page.fill("#typeMemberInputId", "cease2504")
#             page.fill("#typeMemberInputPassword", "asdf12!@")
#             page.click("#btn_memberLogin")
#
#             # state.json 저장
#             context.storage_state(path=STATE_PATH)
#             browser.close()
#     return STATE_PATH
#
#
# @pytest.fixture(scope="function")
# def page(ensure_login_state):
#     """로그인 상태가 보장된 페이지 fixture"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state=ensure_login_state)
#         page = context.new_page()
#         yield page
#         context.close()
#         browser.close()
