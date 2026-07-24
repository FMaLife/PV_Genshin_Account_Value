import pandas as pd
import requests
from bs4 import BeautifulSoup

INPUT_PATH = "data/raw/G8_character_tiers.csv"
OUTPUT_PATH = "data/raw/G8_character_info.csv"

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
}

def fetch_html(url: str) -> str:

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.text

def parse_rarity(html: str) -> int:

    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr")

    for row in rows:

        th = row.find("th")

        if th and th.get_text(strip=True) == "Rarity":

            stars = row.find("td").get_text(strip=True)

            return len(stars)

    return None

def parse_recommended_constellation(html: str) -> str:

    soup = BeautifulSoup(html, "html.parser")

    headers = soup.find_all(["h2", "h3"])

    for header in headers:

        text = header.get_text(" ", strip=True)

        if "Best Constellation Rating" not in text:
            continue

        table = header.find_next("table")

        best_constellation = "C0"

        for row in table.find_all("tr")[1:]:

            constellation = row.find("th").get_text(strip=True)
            rating = row.find("td").get_text(strip=True)

            if rating == "★★★":
                return constellation

        return best_constellation

    return "C0"

def main():

    df = pd.read_csv(INPUT_PATH)

    rarities = []
    recommendations = []

    for i, row in df.iterrows():

        print(f"[{i+1}/{len(df)}] {row['character_name']}")

        html = fetch_html(row["character_url"])

        rarities.append(parse_rarity(html))
        recommendations.append(
            parse_recommended_constellation(html)
        )

    df["rarity"] = rarities
    df["recommended_constellation"] = recommendations

    print(df.head())
    print(df.isnull().sum())

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()