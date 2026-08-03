"""
Scrape Character Tier data from Game8 C0 Tier List.

Output:
    data/raw/G8_character_tiers.csv
"""

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

TIER_LIST_URL = "https://game8.co/games/Genshin-Impact/archives/297465"

OUTPUT_PATH = "data/raw/G8_character_tiers.csv"

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
}


# --------------------------------------------------------------------
# Download HTML
# --------------------------------------------------------------------

def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


# --------------------------------------------------------------------
# Parse Tier Table
# --------------------------------------------------------------------

def parse_tier_table(html: str):

    roles = ["Main DPS", "Sub-DPS", "Support"]

    soup = BeautifulSoup(html, "html.parser")

    records = []

    # หาเฉพาะตาราง Tier (Main / C0 / C6)
    tier_tables = []

    for table in soup.find_all("table"):

        headers = [th.get_text(strip=True) for th in table.find_all("th")]

        if headers[:4] == ["", "Main DPS", "Sub-DPS", "Support"]:
            tier_tables.append(table)

    if len(tier_tables) < 2:
        raise RuntimeError("C0 tier table not found.")

    # ตารางที่ 2 คือ C0 Tier List
    tier_table = tier_tables[1]

    rows = tier_table.find_all("tr")[1:]

    for row in rows:

        tier_img = row.find("th").find("img")

        if tier_img is None:
            continue

        tier = tier_img["alt"].replace(" Tier", "")

        cells = row.find_all("td")

        for role, cell in zip(roles, cells):

            links = cell.find_all("a", class_="a-link")

            for link in links:

                url = link.get("href")

                image = link.find("img")

                if image is None:
                    continue

                name = image.get("alt", "")

                name = (
                    name.replace("Genshin - ", "")
                    .replace(" DPS Rank", "")
                    .replace(" Sub-DPS Rank", "")
                    .replace(" Support Rank", "")
                    .strip()
                )

                # ตัด constellation suffix C0 ที่ติดมากับ alt text
                name = re.sub(r"\s+C\d$", "", name).strip()

                # Skip Traveler variants
                if name.startswith("Traveler"):
                    continue

                records.append({
                    "character_name": name,
                    "role": role,
                    "tier": tier,
                    "character_url": url
                })

    return records


# --------------------------------------------------------------------
# Export CSV
# --------------------------------------------------------------------

def export_csv(records, output_path: str):

    df = pd.DataFrame(records)

    df.to_csv(output_path, index=False)


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main():

    print("Downloading Game8 C0 Tier List...")

    html = fetch_html(TIER_LIST_URL)

    print("Parsing HTML...")

    records = parse_tier_table(html)

    print(f"Found {len(records)} records")

    export_csv(records, OUTPUT_PATH)

    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()