"""
Scrape Character Tier data from Game8.

Output:
    data/raw/G8_character_tiers.csv
"""

import pandas as pd
import requests
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
    """
    Download webpage HTML.
    """

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.text


# --------------------------------------------------------------------
# Parse Tier Table
# --------------------------------------------------------------------

def parse_tier_table(html: str):
    """
    Parse Game8 tier table.
    """

    roles = [ "Main DPS", "Sub-DPS", "Support" ]

    soup = BeautifulSoup(html, "html.parser")

    records = []

    # หา table ทั้งหมด
    tables = soup.find_all("table")

    print(f"Found {len(tables)} tables")

    # ----------------------------
    # ใช้เฉพาะ Tier Table
    # ----------------------------
    tier_table = tables[2]

    rows = tier_table.find_all("tr")[1:]

    print(f"Rows = {len(rows)}")

    # บันทึกไว้เปิดดูใน VSCode
    with open("table_1.html", "w", encoding="utf-8") as f:
        f.write(tier_table.prettify())

    print("Saved table_1.html")

    for row in rows:

        tier_img = row.find("th").find("img")

        tier = tier_img["alt"].replace(" Tier", "")

        print(tier)

        cells = row.find_all("td")

        print(len(cells))

        for role, cell in zip(roles, cells):

            links = cell.find_all("a", class_="a-link")

            for link in links:

                url = link.get("href")

                image = link.find("img")

                if image is None:
                    continue

                # ดึงชื่อจาก alt
                name = image.get("alt", "")

                # ทำความสะอาดชื่อ
                name = (
                    name.replace("Genshin - ", "")
                    .replace(" DPS Rank", "")
                    .replace(" Sub-DPS Rank", "")
                    .replace(" Support Rank", "")
                    .strip()
                )  

                records.append({
                    "character_name": name,
                    "role": role,
                    "tier": tier,
                    "character_url": url
                })


    for i, table in enumerate(tables):
        headers = [th.get_text(strip=True) for th in table.find_all("th")[:4]]
        print(i, headers)

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

    print("Downloading Game8 Tier List...")

    html = fetch_html(TIER_LIST_URL)

    print("Parsing HTML...")

    records = parse_tier_table(html)

    print(f"\nFound {len(records)} records")

    export_csv(records, OUTPUT_PATH)

    print("Done.")


if __name__ == "__main__":
    main()