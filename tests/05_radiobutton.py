from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.set_content('''
        <label><input type="radio" name="plan" value="basic"> Basic</label>
        <label><input type="radio" name="plan" value="pro"> Pro</label>
    ''')
    pro = page.locator('[name="plan"][value="pro"]')
    pro.check()
    assert pro.is_checked()
    assert not page.locator('[name="plan"][value="basic"]').is_checked()
    browser.close()

print("Radio button test passed")
