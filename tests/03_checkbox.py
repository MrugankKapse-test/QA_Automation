from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.set_content('<label><input id="terms" type="checkbox"> Accept terms</label>')
    checkbox = page.locator("#terms")
    checkbox.check()
    assert checkbox.is_checked()
    checkbox.uncheck()
    assert not checkbox.is_checked()
    browser.close()

print("Checkbox test passed")
