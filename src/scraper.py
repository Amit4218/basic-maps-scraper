from playwright.sync_api import Page, sync_playwright
from rich.console import Console
from rich.prompt import Prompt

from src.utils import read_links, write_links_in_chunk, write_to_file

console = Console()


def scroll_sidebar(page: Page, filename: str):
    """scroll the sidebar until the end of the list"""
    sidebar = page.locator('div[role="feed"]')
    with console.status("[bold cyan][Scrolling Sidebar Results...][/]"):
        previous_height = 0
        links = []

        while True:
            if len(links) >= 5:
                write_links_in_chunk(links, filename)
                links = []

            sidebar.evaluate("(el) => el.scrollTo(0, el.scrollHeight)")
            page.wait_for_timeout(2000)

            current_height = sidebar.evaluate("(el) => el.scrollHeight")

            if current_height == previous_height:
                break

            previous_height = current_height

            all_links = page.locator("a.hfpxzc").all()

            for link in all_links:
                links.append(link.get_attribute("href"))


def safe_get_attribute(page, selector, attribute):
    """helper to scrape the information safely"""
    locator = page.locator(selector)
    if locator.count() > 0:
        return locator.first.get_attribute(attribute)
    return None


def scrape_info(page, filename: str, url: str | None = None):
    """scrapes the basic list information"""
    if url:
        page.goto(url)
        page.wait_for_timeout(3000)

    # when scraping for a business and multiple results are found
    multiple_results = page.locator("a.hfpxzc").all()
    links = []

    if len(multiple_results) > 1:
        # append all the resturents link
        for link in multiple_results:
            links.append(link.get_attribute("href"))

        # ask the user if they want to continue
        choice = Prompt.ask(
            f"{len(multiple_results)} extra results found, continue and scrape all? \nN -> scrape only the first result ",
            choices=["Y", "N"],
            default="Y",
        )

        if choice == "Y":
            with console.status("[bold cyan][Scraping extra links][/]"):
                for link in links:
                    scrape_info(page, url=link, filename=filename)
                    return
        else:
            first_result = multiple_results[0].get_attribute("href")
            scrape_info(page, filename, url=first_result)
            return

    try:
        name = page.locator("h1").first.text_content()
        console.print(f"[bold cyan][Srcaping][/][bold blue] {name}[/]")

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
            "url": url if url else None,
        }

        write_to_file(data, filename)
    except Exception as e:
        console.print(f"[bold red][Error] scraping[/] [bold red]{url}: {e}[/]")


def fill_input_form(query, page):
    """finds the input form and searches for the provided query"""
    page.wait_for_selector("form")
    form = page.locator("form.NhWQq").locator("input")
    form.fill(query)
    form.press("Enter")


def scrape_using_keyword(keyword: str, place: str, headless: bool = True):
    """scrapes all the listed links and info after keword search"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_context().new_page()

        console.print(
            f"\n[bold green] Scraping started for {place} searching {keyword}[/]"
        )

        page.goto("https://maps.google.com")

        # search the place
        fill_input_form(place, page)
        page.wait_for_timeout(5000)

        # search the keyword
        fill_input_form(keyword, page)
        page.wait_for_timeout(5000)

        # scroll sidebar
        scroll_sidebar(page, keyword)

        # prompt the user if they want to continue or stop after links
        choice = Prompt.ask(
            f"All links fetched, Continue with scraping {keyword} data? : ",
            choices=["Yes", "No"],
            default="Yes",
        )

        if choice.lower() == "yes":
            links = read_links(keyword)

            with console.status(
                f"[bold cyan][Scraping {keyword} information now...][/]"
            ):
                for link in links:
                    scrape_info(page=page, url=link, filename=keyword)

                console.print(
                    f"[bold green]Existing...[/] [bold yellow]scraped information available in results/{keyword}.json[/]"
                )

        else:
            console.print(
                f"[bold green]Existing...[/] [bold yellow]links can be found in link-{keyword}.json[/]"
            )


def scrape_only_business(business_name: str, headless: bool = False):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_context().new_page()

        console.print(f"[bold green] Scraping started for {business_name}[/]")
        page.goto("https://maps.google.com")
        page.wait_for_timeout(5000)

        fill_input_form(business_name, page)
        page.wait_for_timeout(5000)
        scrape_info(page, filename=business_name)

        console.print(
            f"[bold green] Scraping completed file can be found in results/{business_name}.json file[/]"
        )
