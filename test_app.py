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

def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(playwright):
    playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
    capabilities['LT:Options']['playwrightVersion'] = playwrightVersion

    lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(
        json.dumps(capabilities))
    browser = playwright.chromium.connect(lt_cdp_url)
    page = browser.new_page()
    page.set_viewport_size({"width": 1600, "height": 1200})
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
    get_started = page.locator("text=Get Started")
    expect(get_started).to_have_attribute("href", "/docs/intro")
    get_started.click()
    expect(page).to_have_url(re.compile(".*intro"))
    page.goto('https://pptr.dev/')
    clickOnElement(page, 'guides/')
    clickOnElement(page, 'api/')
    sleep(4)
    clickOnElement(page, 'api/puppeteer.accessibility')
    clickOnElement(page, 'api/puppeteer.accessibility.snapshot')
    clickOnElement(page, 'api/puppeteer.actionresult')
    clickOnElement(page, 'api/puppeteer.awaitable')
    clickOnElement(page, 'api/puppeteer.boundingbox.height')
    clickOnElement(page, 'api/puppeteer.boundingbox')
    clickOnElement(page, 'api/puppeteer.boundingbox.width')
    clickOnElement(page, 'api/puppeteer.boxmodel.border')
    clickOnElement(page, 'api/puppeteer.boxmodel.content')
    clickOnElement(page, 'api/puppeteer.boxmodel.height')
    clickOnElement(page, 'api/puppeteer.boxmodel.margin')
    clickOnElement(page, 'api/puppeteer.boxmodel')
    clickOnElement(page, 'api/puppeteer.boxmodel.padding')
    clickOnElement(page, 'api/puppeteer.boxmodel.width')
    clickOnElement(page, 'api/puppeteer.browser.browsercontexts')
    clickOnElement(page, 'api/puppeteer.browser.close')
    page.goto('https://pptr.dev/')
    clickOnElement(page, 'api/')
    clickOnElement(page, 'api/puppeteer.browser.createincognitobrowsercontext')
    clickOnElement(page, 'api/puppeteer.browser.defaultbrowsercontext')
    clickOnElement(page, 'api/puppeteer.browser.disconnect')
    clickOnElement(page, 'api/puppeteer.browser.isconnected')
    clickOnElement(page, 'api/puppeteer.browser')
    clickOnElement(page, 'api/puppeteer.browser.newpage')
    clickOnElement(page, 'api/puppeteer.browser.pages')
    clickOnElement(page, 'api/puppeteer.browser.process')
    clickOnElement(page, 'api/puppeteer.browser.target')
    clickOnElement(page, 'api/puppeteer.browser.targets')
    clickOnElement(page, 'api/puppeteer.browser.useragent')
    clickOnElement(page, 'api/puppeteer.browser.version')
    #Lambdatest sample app test
    page.goto('https://lambdatest.github.io/sample-todo-app/')
    page.locator('body > div > div > div > ul > li:nth-child(1) > input').click()
    page.locator('body > div > div > div > ul > li:nth-child(2) > input').click()
    page.locator('body > div > div > div > ul > li:nth-child(3) > input').click()
    page.locator('body > div > div > div > ul > li:nth-child(4) > input').click()
    page.locator('body > div > div > div > ul > li:nth-child(5) > input').click()
    page.locator('#sampletodotext').fill('Hypertest LambdaTest')
    page.locator('#addbutton').click()
    page.locator('body > div > div > div > ul > li:nth-child(6) > input').click()
    page.locator('#sampletodotext').fill('Hypertest LambdaTest')
    page.locator('#addbutton').click()
    page.locator('body > div > div > div > ul > li:nth-child(7) > input').click()
    browser.close()

def clickOnElement(page, name):
    page.locator('[href="/' + name + '"]').first.click()
    sleep(2)

with sync_playwright() as playwright:
    test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(playwright)
