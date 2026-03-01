from typing import Annotated, List

import typer

from src.scraper import scrape_only_business, scrape_using_keyword

app = typer.Typer(help="Basic Google Scraper CLI\n")


@app.command(help="Scrape businesses by keyword and location.")
def keyword(
    place: Annotated[str, typer.Argument(help="Name of the location or place")],
    keyword: Annotated[str, typer.Argument(help="Keyword to search eg: (Restaurants)")],
):
    """
    Search Google using a keyword within a specific place.\n
    Example:
    >>> main.py keyword <placename> <keyword>
    """
    scrape_using_keyword(keyword, place)


@app.command(help="Scrape a specific business by name.")
def business(
    business_name: Annotated[
        List[str],
        typer.Argument(help="Full name of the business eg: (my business)"),
    ],
    scrape_reviews: bool = typer.Option(
        False,
        "--reviews",
        help="scrape all the reviews (not implemented)",
    ),
    scrape_images: bool = typer.Option(
        False, "--images", help="scrapes all the listed images link (not implemented)"
    ),
):
    """
    Search and scrape a single business.
    Example:
    >>> main.py keyword <businessname>
    """
    business = " ".join(business_name)
    scrape_only_business(business, headless=False)


if __name__ == "__main__":
    app()
