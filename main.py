from typing import Annotated, List

import typer

from src.scraper import scrape_only_business, scrape_using_keyword

app = typer.Typer()


@app.command()
def keyword(
    place: Annotated[str, typer.Argument(help="name of the location or place")],
    keyword: Annotated[
        str, typer.Argument(help="keyword to search (example Resturants)")
    ],
):
    scrape_using_keyword(keyword, place)


@app.command()
def business(
    business_name: Annotated[List[str], typer.Argument(help="Name of the business")],
):
    business = " ".join(business_name)
    scrape_only_business(business, headless=False)


if __name__ == "__main__":
    app()
