from playwright.sync_api import Playwright
from scrapy import Selector
from Utils import *
import time
import json
import os


class Scraper:

    def __init__(self, playwright: Playwright, filenm: str):
        self.browser = playwright.firefox.launch(headless=False)
        self.context = self.browser.new_context()
        self.context.set_default_timeout(timeout=90000)
        self.page = self.context.new_page()
        self.filenm = filenm
        self.cmp = []
        self.count = 0

    def save_data(self):
        if not os.path.exists("Output"):
            os.mkdir("Output")
        with open(f"Output/{self.filenm}.json", "w") as f:
            json.dump(self.cmp, f)

    def start(self):
        for link in websites:
            print(f"URL ====> {link}")
            self.get_data(link)
            self.save_data()
        self.context.close()
        self.browser.close()
        print("Completed!")

    def get_response(self):
        while True:
            try:
                return Selector(text=self.page.content())
            except:
                pass

    def goto_link(self, link: str):
        while True:
            try:
                self.page.goto(link)
                time.sleep(1)
                break
            except:
                self.page.close()
                self.page = self.context.new_page()

    def wait_element(self, xpath: str):
        x = 0
        while True:
            response = self.get_response()
            if response.xpath(xpath):
                break
            if x > 4:
                break
            time.sleep(2)
            x += 1

    def get_data(self, link: str):
        self.goto_link(link)
        self.wait_element("//iframe[contains(@id, 'ads_iframe')] | //a[contains(@href, 'advertisement') and .//img]")
        fnl = {
            "page_url": link,
            "a_tags": []
        }
        for frame in self.page.frames:
            resp = Selector(text=frame.content())
            for item in resp.xpath("//a[.//img]"):
                fnl.get("a_tags").append(item.get())
        response = self.get_response()
        for item in response.xpath("//a[contains(@href, 'advertisement') and .//img]"):
            fnl.get("a_tags").append(item.get())
        self.cmp.append(fnl)
        self.count += 1
        print(f"Scraped ------------------> {self.count}")