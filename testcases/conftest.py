import allure
import os
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import Error as PlaywrightError, sync_playwright
from utilities import configReader


SUPPORTED_BROWSERS = ["chrome", "firefox"]
SELECTED_BROWSERS = [
    browser.strip()
    for browser in os.getenv("BROWSERS", "chrome").split(",")
    if browser.strip()
]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(params=SELECTED_BROWSERS, scope="function")
def browser(request):
    browser_type = request.param.lower()
    headless = os.getenv("HEADLESS", "false").lower() == "true"

    if browser_type not in SUPPORTED_BROWSERS:
        raise ValueError(
            f"Unsupported browser: {browser_type}. "
            f"Choose from: {', '.join(SUPPORTED_BROWSERS)}"
        )

    with sync_playwright() as p:
        if browser_type == "chrome":
            launched_browser = p.chromium.launch(headless=headless)
        else:
            launched_browser = p.firefox.launch(headless=headless)

        yield launched_browser
        launched_browser.close()


@pytest.fixture(autouse=True)
def setup_function(page):
    page.goto(
        configReader.readConfig("basic info", key="testsiteurl"),
        wait_until="domcontentloaded",
        timeout=60000,
    )


@pytest.fixture(scope="function")
def page(browser, request):
    os.makedirs("traces", exist_ok=True)
    context = browser.new_context(
        record_video_dir="videos/",
        viewport={"width": 1920, "height": 1080},
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    current_page = context.new_page()

    yield current_page

    trace_path = os.path.join("traces", f"{request.node.name}.zip")
    try:
        context.tracing.stop(path=trace_path)
    except PlaywrightError:
        pass
    finally:
        context.close()


@pytest.fixture()
def log_on_failure(request, page):
    yield

    if (
        getattr(request.node, "rep_call", None)
        and request.node.rep_call.failed
        and not page.is_closed()
    ):
        os.makedirs("screenshot", exist_ok=True)
        allure.attach(
            page.screenshot(full_page=True),
            name=f"failure-{request.node.name}",
            attachment_type=AttachmentType.PNG
        )
