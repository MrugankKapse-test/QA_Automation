from pathlib import Path

from playwright.sync_api import sync_playwright


PRACTICE_URL = "https://rahulshettyacademy.com/AutomationPractice/"
SCREENSHOT_PATH = Path(__file__).parent / "challenge.png"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)

    try:
        page = browser.new_page()
        page.goto(PRACTICE_URL, wait_until="domcontentloaded")

        page.locator("#autocomplete").fill("Himanshu")
        page.locator('input[value="radio3"]').check()
        page.locator("#checkBoxOption2").check()
        page.locator("#dropdown-class-example").select_option("option3")

        page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        print(f"Screenshot saved to {SCREENSHOT_PATH}")
    finally:
        browser.close()
