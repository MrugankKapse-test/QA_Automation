from playwright.sync_api import sync_playwright
from pathlib import Path


URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

DOWNLOAD_DIR = Path(
    "/Users/mrugankkapse/Documents/Playwright_Project/QA_Automation/downloads"
)


with sync_playwright() as p:

    print("Opening OrangeHRM...")

    browser = p.chromium.launch(
        headless=False,
        slow_mo=500
    )

    context = browser.new_context(
        accept_downloads=True
    )

    page = context.new_page()

    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(60000)

    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------
    # 1. Open OrangeHRM
    # ---------------------------------------

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("OrangeHRM opened")

    # ---------------------------------------
    # 2. Login
    # ---------------------------------------

    page.get_by_placeholder("Username").fill("Admin")

    page.get_by_placeholder("Password").fill("admin123")

    page.get_by_role(
        "button",
        name="Login"
    ).click(no_wait_after=True)

    page.wait_for_url(
        "**/dashboard/index",
        timeout=60000
    )

    print("Login successful")

    # ---------------------------------------
    # 3. Click Recruitment
    # ---------------------------------------

    page.get_by_text(
        "Recruitment",
        exact=True
    ).click(no_wait_after=True)

    page.wait_for_url(
        "**/recruitment/viewCandidates",
        timeout=60000
    )

    print("Recruitment page opened")

    # ---------------------------------------
    # 4. Click Candidates
    # ---------------------------------------
    #
    # IMPORTANT:
    # There are two "Candidates" elements:
    #
    # 1. Candidates link
    # 2. Candidates heading
    #
    # Therefore use get_by_role("link")
    # ---------------------------------------

    candidates_link = page.get_by_role(
        "link",
        name="Candidates"
    )

    candidates_link.click(
        no_wait_after=True
    )

    page.wait_for_url(
        "**/recruitment/viewCandidates",
        timeout=60000
    )

    print("Candidates page opened")

    page.wait_for_timeout(2000)

    # ---------------------------------------
    # 5. Check candidate records
    # ---------------------------------------

    rows = page.locator(
        ".oxd-table-card"
    )

    row_count = rows.count()

    print(
        "Candidate records found:",
        row_count
    )

    if row_count == 0:

        print("No candidate records available")

    else:

        print("Candidate records are available")

        # ---------------------------------------
        # 6. Open first candidate
        # ---------------------------------------

        first_row = rows.first

        first_row.click(
            no_wait_after=True
        )

        page.wait_for_timeout(2000)

        print("Candidate profile opened")

        # ---------------------------------------
        # 7. Find download buttons
        # ---------------------------------------

        download_buttons = page.get_by_text(
            "Download",
            exact=True
        )

        count = download_buttons.count()

        print(
            "Download buttons found:",
            count
        )

        # ---------------------------------------
        # 8. Download files
        # ---------------------------------------

        if count > 0:

            for i in range(count):

                button = download_buttons.nth(i)

                if button.is_visible():

                    print(
                        f"Downloading file {i + 1}..."
                    )

                    with page.expect_download(
                        timeout=30000
                    ) as download_info:

                        button.click()

                    download = download_info.value

                    filename = download.suggested_filename

                    filepath = (
                        DOWNLOAD_DIR / filename
                    )

                    download.save_as(
                        str(filepath)
                    )

                    print(
                        "Downloaded:",
                        filepath
                    )

        else:

            print(
                "No Download button available "
                "for this candidate."
            )

    # ---------------------------------------
    # 9. Keep browser open temporarily
    # ---------------------------------------

    page.wait_for_timeout(5000)

    browser.close()

    print("Browser closed")
