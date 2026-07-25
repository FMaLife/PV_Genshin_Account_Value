import pandas as pd
import requests
from bs4 import BeautifulSoup

OUTPUT_PATH = "data/raw/G8_character_info.csv"
INPUT_PATH = "data/raw/G8_character_tiers.csv"

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


def parse_recommended_constellation(html: str, rarity: int) -> str:

    soup = BeautifulSoup(html, "html.parser")

    headers = soup.find_all(["h2", "h3"])

    for header in headers:

        text = header.get_text(" ", strip=True)

        # รองรับทั้ง
        # Best Constellation Rating
        # Best Constellation Rating and Explanation
        if "Best Constellation" not in text:
            continue

        table = header.find_next("table")

        if table is None:
            break

        ratings = []

        for row in table.find_all("tr")[1:]:

            th = row.find("th")
            td = row.find("td")

            if th is None or td is None:
                continue

            constellation = th.get_text(strip=True)
            rating = td.get_text(" ", strip=True)

            if "★★★" in rating:
                stars = 3
            elif "★★☆" in rating:
                stars = 2
            elif "★☆☆" in rating:
                stars = 1
            else:
                stars = 0

            ratings.append((constellation, stars))

        # ----------------------------
        # 5★ Characters
        # ----------------------------
        if rarity == 5:

            for constellation, stars in ratings:

                if constellation in ["C1", "C2"] and stars == 3:
                    return constellation

            return "C0"

        # ----------------------------
        # 4★ Characters
        # ----------------------------
        else:

            best = "C0"

            for constellation, stars in ratings:

                if stars == 3:
                    best = constellation

            return best

    # ถ้าไม่พบหัวข้อ Best Constellation
    return "C0"

def main():

    df = pd.read_csv(INPUT_PATH)

    rarities = []
    recommendations = []

    for i, row in df.iterrows():

        print(f"[{i+1}/{len(df)}] {row['character_name']}")

        html = fetch_html(row["character_url"])

        rarity = parse_rarity(html)

        rarities.append(rarity)

        recommendations.append(
            parse_recommended_constellation(html, rarity)
        )

    df["rarity"] = rarities
    df["recommended_constellation"] = recommendations

    df.to_csv(OUTPUT_PATH, index=False)

    print(df.head())

    print(df.isnull().sum())

    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()