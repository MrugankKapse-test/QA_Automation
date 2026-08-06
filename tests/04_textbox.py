from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.set_content('<label>Name <input id="name" type="text"></label>')
    textbox = page.locator("#name")
    textbox.fill("Himanshu")
    assert textbox.input_value() == "Himanshu"
    browser.close()

print("Textbox test passed")
