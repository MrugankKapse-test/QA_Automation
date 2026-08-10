from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=500
    )

    page = browser.new_page()

    # Increase timeout for OrangeHRM
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(60000)

    # 1. Open OrangeHRM
    print("Opening OrangeHRM...")

    page.goto(
        "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("OrangeHRM opened")

    # 2. Login
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")

    page.get_by_role("button", name="Login").click()

    # Wait for dashboard
    page.locator("h6").filter(has_text="Dashboard").wait_for(
        state="visible",
        timeout=30000
    )

    print("Login successful")

    # 3. Click Leave
    leave = page.get_by_text("Leave", exact=True)

    leave.wait_for(
        state="visible",
        timeout=30000
    )

    leave.click(
        no_wait_after=True
    )

    # 4. Wait for Leave page
    page.locator("h6").filter(has_text="Leave").wait_for(
        state="visible",
        timeout=30000
    )

    print("Leave page opened")

    # 5. Click Search
    search_button = page.get_by_role(
        "button",
        name="Search"
    )

    search_button.wait_for(
        state="visible",
        timeout=30000
    )

    search_button.click(
        no_wait_after=True
    )

    # 6. Wait for search result
    page.wait_for_timeout(3000)

    # 7. Check "No Records Found"
    no_records = page.locator(
        "span",
        has_text="No Records Found"
    ).first

    if no_records.is_visible():

        print("No Records Found")
        print("No Records Found message detected")

        # 8. Take screenshot
        page.screenshot(
            path="/Users/mrugankkapse/Documents/Playwright_Project/test/no_records_found.png",
            full_page=True
        )

        print("Screenshot saved")

    else:

        print("Records are available")

    # Keep browser open for 3 seconds
    page.wait_for_timeout(3000)

    browser.close()
