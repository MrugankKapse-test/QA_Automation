from pathlib import Path

from playwright.sync_api import expect, sync_playwright


FORM_URL = (Path(__file__).parent / "registration_form.html").resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=False)
    page = browser.new_page()
    page.goto(FORM_URL)

    # Verify validation is displayed for an incomplete form.
    page.get_by_role("button", name="Register").click()
    expect(page.locator("#message")).to_have_text(
        "Please complete all required fields and choose at least one hobby."
    )

    page.locator("#first-name").fill("Himanshu")
    page.locator("#last-name").fill("Prakash")
    page.locator("#email").fill("himanshu@example.com")
    page.locator("#password").fill("SecurePass123")
    page.locator('[name="gender"][value="male"]').check()
    page.locator('[name="hobbies"][value="reading"]').check()
    page.locator('[name="hobbies"][value="music"]').check()
    page.locator("#country").select_option("india")
    page.get_by_role("button", name="Register").click()

    expect(page.locator("#message")).to_have_text(
        "Registration successful for Himanshu Prakash."
    )
    page.wait_for_timeout(5000)  # Keep the completed form visible during local runs.
    browser.close()

print("Registration automation passed")
