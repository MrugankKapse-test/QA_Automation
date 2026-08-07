from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

with sync_playwright() as p:

    browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=800)
    page = browser.new_page()

    # open the login page
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login", wait_until="domcontentloaded")

    # wait until username field loads
    page.wait_for_selector("input[name='username']", timeout=30000)

    # screenshot before login
    page.screenshot(path=str(SCREENSHOT_DIR / "orangehrm_01_login.png"))

    # fill username
    page.locator("input[name='username']").fill("Admin")

    # press tab to jump to password field
    page.keyboard.press("Tab")

    # fill password
    page.locator("input[name='password']").fill("admin123")

    # press enter to submit
    page.keyboard.press("Enter")

    # wait for dashboard to load
    page.locator(".oxd-topbar-header-title").wait_for(state="visible", timeout=15000)

    # validate title, url, header text, and profile visibility
    assert "OrangeHRM" in page.title()
    assert "/dashboard/index" in page.url
    assert "Dashboard" in page.locator(".oxd-topbar-header-title").text_content()
    assert page.locator(".oxd-userdropdown-tab").is_visible()

    # hover over sidebar menus
    page.locator("a.oxd-main-menu-item:has-text('Admin')").hover()
    page.locator("a.oxd-main-menu-item:has-text('PIM')").hover()
    page.locator("a.oxd-main-menu-item:has-text('Leave')").hover()

    # screenshot after login
    page.screenshot(path=str(SCREENSHOT_DIR / "orangehrm_02_dashboard.png"), full_page=True)

    browser.close()

print("All assertions passed!")
