# Basic Google Maps Scraper

A simple Google Maps scraper built with **Python** and **Playwright** that extracts basic business information and saves it into JSON files.

The scraper collects the following information:

- Name
- Address
- Phone number
- Website URL
- Google Maps URL

Data is scraped based on a provided **state name** and predefined category tags.

---

## Default Tags

By default, the scraper searches for the following categories:

- Restaurants
- Hotels
- Things to do
- Museums
- Transit
- Pharmacies
- ATMs

You can also provide a custom tag when running the script.

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

The project consists of a single file:

```
main.py
```

It accepts:

- **1 required argument** → `state_name`
- **1 optional argument** → `--tag` (custom category)

---

### Run with default tags

```bash
uv run main.py <state_name>

# or

python main.py <state_name>
```

This will scrape all default tags for <state_name>.

---

### Run with a custom tag

```bash
uv run main.py <state_name> --tag <tag>
# or
python main.py <state_name> --tag <tag>
```

Note:
When you provide a custom tag, it is **added to the default tags list**, not replaced.

---

## Output

Results are saved inside a `results/` directory.

Each tag generates a separate JSON file:

```
results/
│── Restaurants.json
│── Hotels.json
│── Museums.json
│── ...
```

Each file contains a JSON array of scraped business objects.

---

## Concurrency

The scraper uses Python’s `ThreadPoolExecutor` to scrape multiple tags concurrently.

- The number of worker threads equals the number of active tags.
- By default, that means **7 concurrent workers**.
- If you add a custom tag, the worker count increases accordingly.

---

## Disclaimer

This project is intended for **educational purposes only**.

Web scraping may violate Google’s Terms of Service.
Use responsibly and at your own risk.

---
