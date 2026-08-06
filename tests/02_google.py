import os

from playwright.sync_api import sync_playwright

# Set GOOGLE_URL to exercise a real search page on a network-enabled machine.
url = os.getenv("GOOGLE_URL", "data:text/html,<title>Google Search</title><input name=q>")

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.goto(url)
    if url.startswith("data:"):
        page.locator("[name=q]").fill("Playwright")
        assert page.locator("[name=q]").input_value() == "Playwright"
    else:
        assert "Google" in page.title()
    browser.close()

print("Search page test passed")
