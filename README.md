# Basic Google Maps Scraper

A simple Google Maps scraper built with **Python** and **Playwright** that extracts basic business information and saves it into JSON files.

The scraper collects the following information:

- Name
- Address
- Phone number
- Website URL
- Google Maps URL
---

## Installation

### Clone the repository

```bash
git clone https://github.com/Amit4218/basic-maps-scraper
cd basic-maps-scraper
```

---

### Install dependencies

#### using uv

This project uses **uv** for dependency management.

If you don’t have `uv` installed, install it from:
[https://docs.astral.sh/uv/#highlights](https://docs.astral.sh/uv/#highlights)

Then install the project dependencies:

```bash
uv sync
```

#### using pip

Make virtual enviroment and activate

```bash
# macOs and linux
python3 -m venv .venv

source .venv/bin/activate

# windows
python -m venv .venv

.\venv\Scripts\activate.bat
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Install Playwright browsers

Since this project uses **Playwright** to launch a Chromium browser instance, make sure the browser binaries are installed:

```bash
uv run playwright install
```

If you encounter issues, ensure Playwright is properly installed.

---

## Usage

It accepts: One of these two commands

- **command** `keyword`
  - This command takes two arguments
  - Use when you want get all the available thing based on the keyword
    - **arguments** `placename` `keyword`

- **command** `business`
  - This command takes the one argument and two optional flags
  - Use when you want to fetch information of a specific business
    - **arguments** `businessname`
      - Example: main.py `businessname`
    - **options** `--images` `--reviews`
    - Example: main.py business `--images` `--reviews`
        <p>passing this flags will scrape all the reviews and images of the business (not implemented yet) </p>

---

### Run the application

```bash
# for keyword based searched
uv run main.py keyword <placename> <keyword>
# or
python main.py keyword <placename> <keyword>
```

---

```bash
# for specific business
uv run main.py business `--images` `--reviews`
# or
python main.py business 
```
---
### Results are saved inside a `results/` directory.
---

## Disclaimer

This project is intended for **educational purposes only**.

Web scraping may violate Google’s Terms of Service.
Use responsibly and at your own risk.

---
