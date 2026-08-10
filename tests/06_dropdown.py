from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.set_content('''
        <select id="country">
            <option value="in">India</option>
            <option value="us">United States</option>
        </select>
    ''')
    dropdown = page.locator("#country")
    dropdown.select_option("us")
    assert dropdown.input_value() == "us"
    browser.close()

print("Dropdown test passed")
