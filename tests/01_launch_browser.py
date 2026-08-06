from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.set_content("<title>Launch test</title><h1>Browser launched</h1>")
    assert page.title() == "Launch test"
    browser.close()

print("Browser launch test passed")
