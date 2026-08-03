import pandas as pd
from score_rules import TIER_SCORE, constellation_bonus

CHARACTER_INFO_PATH = "data/raw/G8_character_info.csv"
CHARACTER_TIER_PATH = "data/raw/G8_character_tiers.csv"
CHARACTER_CONSTELLATION_PATH = "data/raw/G8_character_constellations.csv"
PLAYER_OWNED_PATH = "data/raw/player_owned_characters.csv"


def calculate_character_score(
    character_name: str,
    tier_group: pd.DataFrame,
    current_constellation: str,
    constellation_map: dict,
) -> dict:
    """
    tier_group: แถวของ character_tier ทั้งหมดของตัวละครตัวนี้ (อาจมีหลาย role)
    current_constellation: constellation ปัจจุบันที่ผู้เล่นมี เช่น "C4"
    constellation_map: {character_name: [(constellation, stars), ...]}
    """
    group = tier_group.copy()
    group["tier_score"] = group["tier"].map(TIER_SCORE)
    group = group.sort_values("tier_score", ascending=False)

    main_score = group.iloc[0]["tier_score"]
    secondary_score = group.iloc[1:]["tier_score"].sum() / 2

    character_constellations = constellation_map.get(character_name, [])
    bonus = constellation_bonus(
        current_constellation,
        character_constellations,
        main_score,
    )

    total = main_score + secondary_score + bonus

    return {
        "character_name": character_name,
        "score": int(round(total)),
        "main_role": group.iloc[0]["role"],
        "main_tier": group.iloc[0]["tier"],
        "current_constellation": current_constellation,
        "constellation_bonus": bonus,
    }


def calculate_account_score(
    tier_df: pd.DataFrame,
    constellation_df: pd.DataFrame,
    owned_df: pd.DataFrame,
):
    """
    เฉพาะตัวละครที่อยู่ใน owned_df (ที่ผู้เล่นมีจริง) เท่านั้นที่จะถูกคิดคะแนน
    """
    constellation_map = (
        constellation_df.groupby("character_name")
        .apply(lambda g: list(zip(g["constellation"], g["stars"])))
        .to_dict()
    )

    owned_lookup = dict(
        zip(owned_df["character_name"], owned_df["current_constellation"])
    )

    results = []
    total_score = 0

    for character_name, current_constellation in owned_lookup.items():
        tier_group = tier_df[tier_df["character_name"] == character_name]

        if tier_group.empty:
            print(f"[skip] ไม่พบข้อมูล tier ของ: {character_name}")
            continue

        result = calculate_character_score(
            character_name,
            tier_group,
            current_constellation,
            constellation_map,
        )
        results.append(result)
        total_score += result["score"]

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return total_score, pd.DataFrame(results)


def main():
    tier_df = pd.read_csv(CHARACTER_TIER_PATH)
    constellation_df = pd.read_csv(CHARACTER_CONSTELLATION_PATH)
    owned_df = pd.read_csv(PLAYER_OWNED_PATH)

    total, result_df = calculate_account_score(tier_df, constellation_df, owned_df)

    print(result_df)
    print(f"\nTotal Score: {total}")


if __name__ == "__main__":
    main()