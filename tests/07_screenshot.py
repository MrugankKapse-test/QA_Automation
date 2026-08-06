from pathlib import Path

from playwright.sync_api import sync_playwright

output = Path(__file__).parent / "screenshots" / "example.png"
output.parent.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 800, "height": 600})
    page.set_content("<title>Screenshot</title><h1>Screenshot test</h1>")
    page.screenshot(path=str(output), full_page=True)
    browser.close()

assert output.is_file() and output.stat().st_size > 0
print(f"Screenshot saved to {output}")
