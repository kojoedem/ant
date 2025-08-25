from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Listen for console events
    page.on("console", lambda msg: print(f"Browser console: {msg.text}"))

    try:
        page.goto("http://127.0.0.1:8000/")
        page.wait_for_load_state('networkidle')
        page.screenshot(path="jules-scratch/verification/01_initial_page.png")

        page.get_by_label("Image").set_input_files('jules-scratch/verification/test_image.png')
        page.fill('input[name="width"]', '100')
        page.fill('input[name="height"]', '100')

        page.click('button[type="submit"]')

        page.wait_for_function("document.querySelector('#output').src.startsWith('blob:')")

        page.screenshot(path="jules-scratch/verification/02_resized_image.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
