"""Day 6: download a candidate resume from OrangeHRM with Playwright."""

from datetime import datetime
from pathlib import Path
import sys

import pytest
from playwright.sync_api import expect, sync_playwright


BASE_URL = "https://opensource-demo.orangehrmlive.com"
PROJECT_ROOT = Path(__file__).parents[1]
RESUME_FILE = PROJECT_ROOT / "test_data" / "sample_resume.pdf"
DOWNLOAD_DIRECTORY = PROJECT_ROOT / "downloads"
SCREENSHOT_PATH = Path(__file__).parent / "screenshots" / "orangehrm_download_triggered.png"


def test_download_candidate_resume() -> None:
    """Create a candidate with a PDF resume, then download that resume."""
    DOWNLOAD_DIRECTORY.mkdir(exist_ok=True)
    SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    candidate_first_name = f"Day6Download{datetime.now():%Y%m%d%H%M%S}"
    candidate_email = f"{candidate_first_name.lower()}@example.com"

    with sync_playwright() as playwright:
        # Launch Microsoft Edge and permit browser downloads.
        browser = playwright.chromium.launch(channel="msedge", headless=False)
        context = browser.new_context(accept_downloads=True, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.set_default_timeout(30_000)

        try:
            # Log in to the OrangeHRM demo application.
            page.goto(f"{BASE_URL}/web/index.php/auth/login", wait_until="domcontentloaded")
            page.locator("input[name='username']").fill("Admin")
            page.locator("input[name='password']").fill("admin123")
            page.get_by_role("button", name="Login").click(no_wait_after=True)
            page.wait_for_url("**/dashboard/index", timeout=60_000)
            expect(page.locator(".oxd-topbar-header-title")).to_contain_text("Dashboard")

            # Open Recruitment > Add Candidate, the verified resume-download workflow.
            page.get_by_role("link", name="Recruitment").click(no_wait_after=True)
            page.wait_for_url("**/recruitment/viewCandidates", timeout=60_000)
            page.get_by_role("button", name="Add").click(no_wait_after=True)
            page.wait_for_url("**/recruitment/addCandidate", timeout=60_000)
            expect(page.get_by_text("Add Candidate", exact=True)).to_be_visible()

            # Populate the required fields and upload the test resume.
            page.locator("input[name='firstName']").fill(candidate_first_name)
            page.locator("input[name='lastName']").fill("Test")
            page.locator("input[placeholder='Type here']").first.fill(candidate_email)
            resume_input = page.locator("input.oxd-file-input[type='file']")
            expect(resume_input).to_be_attached()
            resume_input.set_input_files(RESUME_FILE)
            expect(page.get_by_text(RESUME_FILE.name, exact=True)).to_be_visible()

            # Save the candidate, then identify the actual icon inside its resume filename.
            page.get_by_role("button", name="Save", exact=True).click(no_wait_after=True)
            resume_name = page.get_by_text(RESUME_FILE.name, exact=True)
            expect(resume_name).to_be_visible(timeout=60_000)
            resume_download_control = resume_name.locator(".orangehrm-file-download")
            expect(resume_download_control).to_be_visible(timeout=30_000)

            # Capture the browser download and save it under a meaningful filename.
            with page.expect_download(timeout=30_000) as download_info:
                resume_download_control.click()
            download = download_info.value
            downloaded_file = DOWNLOAD_DIRECTORY / "orangehrm_candidate_resume.pdf"
            download.save_as(downloaded_file)

            # Verify the downloaded file was saved and contains data.
            assert downloaded_file.exists(), "The downloaded resume file was not saved."
            assert downloaded_file.stat().st_size > 0, "The downloaded resume file is empty."

            # Preserve evidence after triggering the download.
            page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        finally:
            # Always release Edge resources.
            context.close()
            browser.close()


if __name__ == "__main__":
    sys.exit(pytest.main(["-q", __file__]))
