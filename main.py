import argparse
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from playwright.sync_api import sync_playwright

# Default tags that will be scraped
TAGS = [
    "Restaurants",
    "Hotels",
    "Things to do",
    "Museums",
    "Transit",
    "Pharmacies",
    "ATMs",
]


def scroll_sidebar(page):
    """scroll the sidebar until the end of the list"""
    sidebar = page.locator('div[role="feed"]')

    previous_height = 0

    while True:
        sidebar.evaluate("(el) => el.scrollTo(0, el.scrollHeight)")
        time.sleep(2)

        current_height = sidebar.evaluate("(el) => el.scrollHeight")

        if current_height == previous_height:
            break

        previous_height = current_height

    links = page.locator("a.hfpxzc").all()
    return [link.get_attribute("href") for link in links if link.get_attribute("href")]


def safe_get_attribute(page, selector, attribute):
    """helper to scrape the information safely"""
    locator = page.locator(selector)
    if locator.count() > 0:
        return locator.first.get_attribute(attribute)
    return None


def scrape_info(page, url):
    """scrapes the basic list information"""
    page.goto(url)
    page.wait_for_timeout(3000)

    data = {}

    try:
        name = page.locator("h1").first.text_content()

        phone = safe_get_attribute(page, 'button[data-item-id^="phone"]', "aria-label")
        address = safe_get_attribute(
            page, 'button[data-item-id="address"]', "aria-label"
        )
        website = safe_get_attribute(page, "a[data-item-id=authority]", "href")

        data = {
            "name": name,
            "address": address,
            "phone": phone,
            "website": website,
            "url": url,
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")

    return data


def write_to_file(data, filename):
    """writes the result data into a json file corsponding to the tag name"""

    if not os.path.exists("results"):
        os.mkdir("results")

    with open(f"results/{filename}.json", "a", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def fill_input_form(query, page):
    """finds the input form and searches for the provided query"""
    page.wait_for_selector("form")
    form = page.locator("form.NhWQq").locator("input")
    form.fill(query)
    form.press("Enter")


def start_scraping(state_name: str, tag: str, headless: bool = True):
    """starts the scraping process"""
    results = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_context().new_page()

        # Navigate to the page
        page.goto("https://maps.google.com")

        # waiting for page to load
        page.wait_for_timeout(5000)

        # search the place
        fill_input_form(state_name, page)

        # search for the tag
        fill_input_form(tag, page)

        # waiting for page to load
        page.wait_for_timeout(5000)

        # scroll_sidebar for all the listing
        links = scroll_sidebar(page)

        # print(f"Found {len(links)} restaurants")

        for link in links:
            info = scrape_info(page, link)
            if info:
                results.append(info)

        browser.close()

    write_to_file(data=results, filename=tag)


def main():
    parser = argparse.ArgumentParser(description="simple google maps scraper")
    parser.add_argument("state", type=str, help="name of the state")
    parser.add_argument(
        "-t",
        "--tag",
        type=str,
        help=f"optional tag default scrapes for {TAGS}",
    )

    args = parser.parse_args()

    state_name = args.state

    if args.tag:
        TAGS.append(args.tag)

    with ThreadPoolExecutor(max_workers=len(TAGS)) as executor:
        for tag in TAGS:
            executor.submit(start_scraping, state_name, tag)


if __name__ == "__main__":
    main()
