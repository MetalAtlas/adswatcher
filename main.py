from playwright.sync_api import sync_playwright
from Ads_Scraper import Scraper

print("Enter Name for Output file:")
filenm = input()

if __name__ == '__main__':
    with sync_playwright() as p:
        s = Scraper(p, filenm)
        s.start()