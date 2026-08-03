TIER_SCORE = {
    "SS": 100,
    "S": 80,
    "A": 60,
    "B": 40,
    "C": 20,
    "D": 10,
}

CONSTELLATION_LEVEL = {
    "C0": 0, "C1": 1, "C2": 2, "C3": 3, "C4": 4, "C5": 5, "C6": 6,
}

# % ของ tier_score ต่อ 1 ระดับ C ที่ผู้เล่นมี (ดาเมจพื้นฐานที่เพิ่มขึ้นเสมอ ไม่ว่าจะติดดาวหรือไม่)
BASE_LEVEL_RATE = 0.02  # 2% ต่อระดับ

# % เพิ่มเติมถ้า C ระดับนั้นติดดาวแนะนำ
STAR_EXTRA_RATE = {
    1: 0.01,
    2: 0.02,
    3: 0.03,
}

# เพดานรวมของ constellation bonus ทั้งหมด (กันไม่ให้เกิน 1 ขั้นเทียร์)
MAX_CONSTELLATION_RATE = 0.20  # 20% ของ tier_score


def constellation_bonus(current_constellation: str, character_constellations: list, tier_score: int) -> int:
    """
    current_constellation: constellation ปัจจุบันของผู้เล่น เช่น "C4"
    character_constellations: list ของ (constellation, stars) ที่ Game8 ติดดาว
        เช่น [("C1", 2), ("C2", 3), ("C4", 2)]
    tier_score: tier_score ของตัวละครตัวนี้ (จาก TIER_SCORE)
    """
    current_level = CONSTELLATION_LEVEL.get(current_constellation, 0)
    starred = dict(character_constellations)

    rate = 0.0
    for lvl in range(1, current_level + 1):
        c = f"C{lvl}"
        rate += BASE_LEVEL_RATE
        if c in starred:
            rate += STAR_EXTRA_RATE.get(starred[c], 0)

    rate = min(rate, MAX_CONSTELLATION_RATE)
    return round(tier_score * rate)