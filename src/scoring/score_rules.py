TIER_SCORE = {
    "SS": 100,
    "S": 80,
    "A": 60,
    "B": 40,
    "C": 20,
    "D": 10,
}

CONSTELLATION_LEVEL = {
    "C0": 0,
    "C1": 1,
    "C2": 2,
    "C3": 3,
    "C4": 4,
    "C5": 5,
    "C6": 6,
}


def constellation_modifier(current: str, recommended: str) -> int:
    current_level = CONSTELLATION_LEVEL.get(current, 0)
    recommended_level = CONSTELLATION_LEVEL.get(recommended, 0)

    if current_level < recommended_level:
        return -20
    elif current_level == recommended_level:
        return 0
    else:
        return 10