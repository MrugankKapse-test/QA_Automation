from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=500
    )

    page = browser.new_page()

    # 1. Open OrangeHRM
    page.goto(
        "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    )

    # 2. Login
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")

    page.get_by_role("button", name="Login").click()

    # 3. Wait for Dashboard
    page.wait_for_url("**/dashboard/index")

    print("Login successful")

    # 4. Click Leave
    page.get_by_text("Leave", exact=True).click()

    # 5. Wait for Leave page
    page.wait_for_url("**/leave/viewLeaveList")

    print("Leave page opened")

    # 6. Click Search
    page.get_by_role("button", name="Search").click()

    # 7. Wait for result
    page.wait_for_timeout(2000)

    # 8. Locate "No Records Found"
    no_records = page.locator("span").filter(
        has_text="No Records Found"
    ).first

    # 9. Check whether it is visible
    if no_records.is_visible():

        print("No Records Found")

        # Capture screenshot
        page.screenshot(
            path="/Users/mrugankkapse/Documents/Playwright_Project/test/no_records_found.png",
            full_page=True
        )

        print("No Records Found message detected")
        print("Screenshot saved")

    else:

        print("Records are available")

    page.wait_for_timeout(3000)

    # 10. Close browser
    browser.close()
