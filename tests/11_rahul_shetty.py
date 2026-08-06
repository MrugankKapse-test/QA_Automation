from pathlib import Path

from playwright.sync_api import sync_playwright


OUTPUT_DIR = Path(__file__).parent / "screenshots"
OUTPUT_DIR.mkdir(exist_ok=True)
SCREENSHOT_PATH = OUTPUT_DIR / "rahul_shetty_practice.png"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice/", wait_until="domcontentloaded")

    page.locator("input#name").fill("Himanshu Raj Prakash")
    page.locator("input[value='radio3']").check()
    page.locator("input#checkBoxOption2").check()
    page.locator("input#checkBoxOption3").check()
    page.locator("select#dropdown-class-example").select_option("option2")

    page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
    print(page.title())

    browser.close()

print(f"Screenshot saved to {SCREENSHOT_PATH}")
