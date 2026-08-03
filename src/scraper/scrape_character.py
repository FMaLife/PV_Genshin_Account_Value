import pandas as pd
import requests
from bs4 import BeautifulSoup

INPUT_PATH = "data/raw/G8_character_tiers.csv"
OUTPUT_PATH = "data/raw/G8_character_info.csv"
CONSTELLATION_OUTPUT_PATH = "data/raw/G8_character_constellations.csv"

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


def parse_constellation_ratings(html: str) -> list:
    """
    คืน list ของ (constellation, stars) ทุกตัวที่มีดาว (stars > 0)
    """
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.find_all(["h2", "h3"])

    for header in headers:
        text = header.get_text(" ", strip=True)
        if "Best Constellation" not in text:
            continue

        # เดินหา table ถัดไปเรื่อยๆ จนกว่าจะเจอตัวที่มีดาวจริง
        for table in header.find_all_next("table"):
            rows = table.find_all("tr")[1:]
            ratings = []
            has_stars = False

            for row in rows:
                th = row.find("th")
                td = row.find("td")
                if th is None or td is None:
                    continue

                constellation = th.get_text(strip=True)
                rating = td.get_text(" ", strip=True)

                if "★" in rating:
                    has_stars = True

                if "★★★" in rating:
                    stars = 3
                elif "★★☆" in rating:
                    stars = 2
                elif "★☆☆" in rating:
                    stars = 1
                else:
                    stars = 0

                if stars > 0:
                    ratings.append((constellation, stars))

            if not has_stars:
                continue  # table นี้ไม่ใช่ table ดาว ข้ามไปหาตัวถัดไป

            return ratings  # อาจเป็น list ว่างถ้าไม่มีตัวไหนติดดาวเลย

    return []


def main():
    tier_df = pd.read_csv(INPUT_PATH)
    char_df = tier_df.drop_duplicates(subset=["character_name"]).reset_index(drop=True)

    rarities = []
    constellation_rows = []

    for i, row in char_df.iterrows():
        name = row["character_name"]
        print(f"[{i+1}/{len(char_df)}] {name}")

        html = fetch_html(row["character_url"])

        rarity = parse_rarity(html)
        rarities.append(rarity)

        for constellation, stars in parse_constellation_ratings(html):
            constellation_rows.append({
                "character_name": name,
                "constellation": constellation,
                "stars": stars,
            })

    char_df["rarity"] = rarities
    char_df.to_csv(OUTPUT_PATH, index=False)

    constellation_df = pd.DataFrame(constellation_rows)
    constellation_df.to_csv(CONSTELLATION_OUTPUT_PATH, index=False)

    print(char_df.head())
    print(char_df.isnull().sum())
    print(f"\nSaved to {OUTPUT_PATH}")
    print(f"Saved to {CONSTELLATION_OUTPUT_PATH}")


if __name__ == "__main__":
    main()