import pytest
import json
import urllib
import subprocess
from playwright.sync_api import sync_playwright

# List of capabilities
CAPABILITIES_LIST = [
    {
        "browserName": "MicrosoftEdge",
        "platform": "macOS Sequoia",
        "name": "Scenario on Edge macOS"
    },
    {
        "browserName": "Chrome",
        "platform": "Windows 11",
        "name": "Scenario on Chrome Windows"
    },
    # {
    #     "browserName": "pw-firefox",
    #     "platform": "macOS Sequoia",
    #     "name": "Scenario on Firefox macOS"
    # },
]

# Base capabilities shared across tests
BASE_CAPABILITIES = {
    "LT:Options": {
        "build": "Run parallel three scenarios on different browsers 2",
        "user": "hanakent66@gmail.com",
        "accessKey": "nvIyg4pNe8gJy5ASUQMZDD6HevOw2euTuOY5Z7W5tbM6Nuzywq",
        "network": True,
        "video": True,
        "console": True,
        "tunnel": False,
    }
}

def connect_browser(capabilities):
    playwright_version = str(subprocess.getoutput("playwright --version")).strip().split(" ")[1]
    capabilities["LT:Options"]["playwrightClientVersion"] = playwright_version
    lt_cdp_url = "wss://cdp.lambdatest.com/playwright?capabilities=" + urllib.parse.quote(json.dumps(capabilities))
    playwright = sync_playwright().start()
    browser = playwright.chromium.connect(lt_cdp_url, timeout=120000)
    return playwright, browser


def set_test_status(page, status, remark):
    page.evaluate(
        "_ => {}",
        f"lambdatest_action: {{\"action\": \"setTestStatus\", \"arguments\": {{\"status\":\"{status}\", \"remark\": \"{remark}\"}}}}"
    )



def scenario_1(page):
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

def scenario_2(page):
    page.goto("https://www.lambdatest.com/selenium-playground/")
    page.wait_for_load_state('networkidle')
    page.locator("text=Drag & Drop Sliders").first.click()
    current_url = page.url
    page.goto(current_url)
    slider_handle = page.locator("#slider3").locator("xpath=//div/input")
    slider_bounds = slider_handle.bounding_box() 
    slider_unit = slider_bounds["width"]/100
    # Drag the slider handle to the 95% position
    expected_value = 0
    i = 0
    while   expected_value<95:
        page.mouse.move(slider_bounds["x"] + i + slider_unit*60, slider_bounds["y"])
        page.mouse.down()
        expected_value = int(page.locator("#rangeSuccess").inner_text())
        i+=slider_unit
    assert expected_value == 95, f"Expected 95, but found {expected_value}"   
    page.wait_for_timeout(2000)

def scenario_3(page):
    page.goto("https://www.lambdatest.com/selenium-playground")
    # page.wait_for_load_state('networkidle')
    page.locator("text=Input Form Submit").first.click()
    current_url = page.url
    page.goto(current_url)
    page.get_by_role("button", name="Submit").click()
    # Assert “Please fill in the fields” error message.
    validation_message = page.evaluate("handle => handle.validationMessage", page.query_selector("#name"))
    # Determine the OS or platform
    platform = page.evaluate("navigator.platform")
    # Define the expected message
    expected_message = (
        "Please fill in this field." if "Mac" in platform else "Please fill out this field."
    )
    assert validation_message == expected_message, f"Expected: {expected_message}, but found: {validation_message}" 
    # Fill in Name, Email, and other fields.
    page.get_by_placeholder("Name").last.fill("Thinh")
    page.get_by_placeholder("Email").last.fill("testerthinh@gmail.com")
    page.get_by_placeholder("Password").last.fill("@abc#")
    page.get_by_placeholder("Company").last.fill("Thinh Company")
    page.get_by_placeholder("Website").last.fill("https://www.lambdatest.com")

    # From the Country drop-down, select “United States” using the text property.
    page.get_by_role("combobox").select_option(value = "United States")

    # Fill in all fields and click “Submit”.
    page.get_by_placeholder("City").last.fill("Ha Noi")
    page.get_by_placeholder("Address 1").last.fill("13 Hang Dao, Hoan Kiem, Ha Noi, VietNam")
    page.get_by_placeholder("Address 2").last.fill("33 Hang Xanh, Ha Noi, VietNam")
    page.get_by_placeholder("State").last.fill("Ha Noi")
    page.get_by_placeholder("Zip code").last.fill("55000")
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Submit").click()

    # Once submitted, validate the success message “Thanks for contacting us, we will get back to you shortly.” on the screen.
    success_msg = page.locator(".success-msg").inner_text()
    assert success_msg == "Thanks for contacting us, we will get back to you shortly.", f"Expected: 'Thanks for contacting us, we will get back to you shortly.', but found: '{success_msg}'"
    page.wait_for_timeout(2000)



@pytest.mark.parametrize("capabilities", CAPABILITIES_LIST)
def test_sequential_scenarios(capabilities):
    # Merge specific capabilities with the base ones
    merged_capabilities = BASE_CAPABILITIES.copy()
    merged_capabilities["browserName"] = capabilities["browserName"]
    merged_capabilities["LT:Options"]["platform"] = capabilities["platform"]
    merged_capabilities["LT:Options"]["name"] = capabilities["name"]

    playwright, browser = connect_browser(merged_capabilities)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    try:
        # Execute scenarios in sequence
        scenario_1(page)
        scenario_2(page)
        scenario_3(page)
        set_test_status(page, "passed", "All scenarios passed successfully")
    except Exception as err:
        set_test_status(page, "failed", str(err))
        raise
    finally:
        context.close()
        browser.close()
        playwright.stop()