import json
import os
from typing import Dict, List


def write_links_in_chunk(links: List[str], filename: str) -> None:
    """Writes links into a links-{filename}.json file"""

    file_path = f"links-{filename}.json"

    existing_links: List[str] = []

    # Read existing data if file exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_links = json.load(f)

    # Merge and remove duplicates while preserving order
    combined_links = list(dict.fromkeys(existing_links + links))

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(combined_links, f, indent=4)


def write_to_file(data: Dict, filename: str):
    """writes result data into a json file corresponding to the filename"""

    file_path = f"results/{filename}.json"

    # Ensure folder exists
    os.makedirs("results", exist_ok=True)

    # Load existing data if file exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    if not isinstance(existing, list):
        existing = [existing]

    # Append new data
    existing.append(data)

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)


def read_links(filename: str):
    """reads the links from the links json file"""
    with open(f"links-{filename}.json", "r", encoding="utf-8") as links:
        results = json.load(links)

    return list(results)
