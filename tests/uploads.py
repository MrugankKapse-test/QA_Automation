"""Day 6: upload an employee attachment in OrangeHRM with Playwright."""

from pathlib import Path
import sys

import pytest
from playwright.sync_api import expect, sync_playwright


BASE_URL = "https://opensource-demo.orangehrmlive.com"
TEST_DATA_DIR = Path(__file__).parents[1] / "test_data"
SCREENSHOT_PATH = Path(__file__).parent / "screenshots" / "orangehrm_attachment_uploaded.png"
SAMPLE_FILE = TEST_DATA_DIR / "sample_upload.pdf"


def test_upload_attachment_to_personal_details() -> None:
    """Upload a PDF through My Info > Personal Details > Attachments."""
    # Create a folder for the successful-upload screenshot.
    SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        # Launch Microsoft Edge as required by the assignment.
        browser = playwright.chromium.launch(channel="msedge", headless=False)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.set_default_timeout(30_000)

        try:
            # Open OrangeHRM and log in with the demo account.
            page.goto(f"{BASE_URL}/web/index.php/auth/login", wait_until="domcontentloaded")
            page.locator("input[name='username']").fill("Admin")
            page.locator("input[name='password']").fill("admin123")

            # Wait explicitly for the dashboard route after submitting the form.
            page.get_by_role("button", name="Login").click(no_wait_after=True)
            page.wait_for_url("**/dashboard/index", timeout=60_000)
            expect(page.locator(".oxd-topbar-header-title")).to_contain_text("Dashboard")

            # Go to My Info > Personal Details, where employee attachments are managed.
            page.get_by_role("link", name="My Info").click()
            page.get_by_role("link", name="Personal Details").click()
            attachments = page.locator(".orangehrm-attachment")
            expect(attachments).to_be_visible()

            # Open the Add Attachment form inside the attachments component.
            attachments.get_by_role("button", name="Add").click()

            # The live OrangeHRM DOM uses: <input type="file" class="oxd-file-input">.
            upload_control = attachments.locator("input.oxd-file-input[type='file']")
            expect(upload_control).to_be_attached()
            upload_control.set_input_files(SAMPLE_FILE)
            attachments.locator("textarea").fill("Day 6 automated PDF upload")

            # Save the file and confirm OrangeHRM reports a successful upload.
            attachments.get_by_role("button", name="Save").click()
            success_toast = page.locator(".oxd-toast--success")
            expect(success_toast).to_be_visible()
            expect(success_toast).to_contain_text("Successfully")

            # Verify that OrangeHRM lists the uploaded filename.
            expect(attachments).to_contain_text(SAMPLE_FILE.name)

            # Save screenshot evidence after successful upload.
            page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        finally:
            # Always close the Edge browser and its context.
            context.close()
            browser.close()


if __name__ == "__main__":
    # Permit direct execution: python tests/13_orangehrm_upload.py
    sys.exit(pytest.main(["-q", __file__]))
