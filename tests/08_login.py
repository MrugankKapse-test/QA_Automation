from playwright.sync_api import sync_playwright

HTML = '''
<form id="login">
  <label>Username <input id="username" required></label>
  <label>Password <input id="password" type="password" required></label>
  <button type="submit">Login</button>
</form>
<p id="message"></p>
<script>
  document.querySelector('#login').addEventListener('submit', event => {
    event.preventDefault();
    document.querySelector('#message').textContent = 'Login successful';
  });
</script>
'''

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.set_content(HTML)
    page.locator("#username").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    assert page.locator("#message").text_content() == "Login successful"
    browser.close()

print("Login test passed")
