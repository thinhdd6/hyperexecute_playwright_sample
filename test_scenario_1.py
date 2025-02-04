import os
import re
import subprocess
import urllib
import json
from os import environ
from time import sleep
from playwright.sync_api import sync_playwright, expect

capabilities = {
    'browserName': 'Chrome',
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': os.environ.get("TARGET_OS"),
        'build': 'Playwright Build',
        'name': 'Playwright Test',
        'user': os.environ.get("LT_USERNAME"),
        'accessKey': os.environ.get("LT_ACCESS_KEY"),
        'network': True,
        'video': True,
        'console': True
    }
}

def test_scenario_1(playwright):
    playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
    capabilities['LT:Options']['playwrightVersion'] = playwrightVersion
    lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(json.dumps(capabilities))
    browser = playwright.chromium.connect(lt_cdp_url)
    page = browser.new_page()
    try:
        timeout = 30000
        page.set_default_navigation_timeout(timeout)
        page.goto("https://www.lambdatest.com/selenium-playground/")
        # page.wait_for_load_state('networkidle')
        page.locator("text=Simple Form Demo").click()
        current_url = page.url
        page.goto(current_url)
        assert "simple-form-demo" in current_url
        enter_message = "Welcome to LambdaTest"
        page.get_by_placeholder("Please enter your Message").fill(enter_message) 
        page.get_by_text("Get Checked Value").first.click()
        your_message = page.locator("xpath=//*[@id='message']").inner_text()
        assert your_message == enter_message,  f"Expected '{your_message}', but found '{enter_message}'"
        page.wait_for_timeout(2000)
    except Exception as err:
        print("Error:: ", err)
        set_test_status(page, "failed", str(err))
    browser.close()

def set_test_status(page, status, remark):
    page.evaluate("_ => {}",
                  "lambdatest_action: {\"action\": \"setTestStatus\", \"arguments\": {\"status\":\"" + status + "\", \"remark\": \"" + remark + "\"}}");

with sync_playwright() as playwright:
    test_scenario_1(playwright)
