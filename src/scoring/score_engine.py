import pandas as pd
from score_rules import TIER_SCORE, constellation_modifier


def calculate_character_score(group: pd.DataFrame,
                              current_constellation: str = "C0"):

    group = group.copy()
    group["tier_score"] = group["tier"].map(TIER_SCORE)

    group = group.sort_values("tier_score", ascending=False)

    main_score = group.iloc[0]["tier_score"]

    secondary_score = group.iloc[1:]["tier_score"].sum() / 2

    recommended = group.iloc[0]["recommended_constellation"]

    modifier = constellation_modifier(
        current_constellation,
        recommended
    )

    total = main_score + secondary_score + modifier

    return {
        "character_name": group.iloc[0]["character_name"],
        "score": int(total),
        "main_role": group.iloc[0]["role"],
        "recommended_constellation": recommended
    }


def calculate_account_score(df: pd.DataFrame):

    results = []

    total_score = 0

    for _, group in df.groupby("character_name"):

        result = calculate_character_score(group)

        results.append(result)

        total_score += result["score"]

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return total_score, pd.DataFrame(results)


if __name__ == "__main__":

    df = pd.read_csv("data/raw/G8_character_info.csv")

    total, result_df = calculate_account_score(df)

    print(result_df.head(20))
    print(f"Total Score: {total}")