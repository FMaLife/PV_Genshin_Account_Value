import pandas as pd
import psycopg2

CHARACTER_INFO_PATH = "data/raw/G8_character_info.csv"
CHARACTER_TIER_PATH = "data/raw/G8_character_tiers.csv"
CHARACTER_CONSTELLATION_PATH = "data/raw/G8_character_constellations.csv"

DB_CONFIG = {
    "host": "localhost",
    "database": "genshin_db",
    "user": "postgres",
    "password": "1412",
    "port": 1412
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def load_character_data(conn, df):
    """
    Insert แต่ละตัวละครลงตาราง character (ไม่มี recommended_constellation แล้ว)
    """
    cursor = conn.cursor()
    character_df = df.drop_duplicates(subset=["character_name"])
    for _, row in character_df.iterrows():
        cursor.execute(
            """
            INSERT INTO character
            (character_name, rarity)
            VALUES (%s, %s);
            """,
            (row["character_name"], row["rarity"])
        )
    cursor.close()


def load_character_tier(conn, tier_df):
    """
    Insert role/tier ของแต่ละตัวละคร (มาจาก G8_character_tiers.csv โดยตรง
    เพราะไฟล์นี้มีครบทุก role ต่อ 1 ตัวละคร ต่างจาก character_info ที่ dedupe ไปแล้ว)
    """
    cursor = conn.cursor()
    for _, row in tier_df.iterrows():
        cursor.execute(
            """
            SELECT character_id
            FROM character
            WHERE character_name = %s;
            """,
            (row["character_name"],)
        )
        result = cursor.fetchone()
        if result is None:
            print(f"[skip] character not found: {row['character_name']}")
            continue
        character_id = result[0]
        cursor.execute(
            """
            INSERT INTO character_tier
            (character_id, role, tier)
            VALUES (%s, %s, %s);
            """,
            (character_id, row["role"], row["tier"])
        )
    cursor.close()


def load_character_constellation(conn, constellation_df):
    cursor = conn.cursor()
    for _, row in constellation_df.iterrows():
        cursor.execute(
            """
            SELECT character_id
            FROM character
            WHERE character_name = %s;
            """,
            (row["character_name"],)
        )
        result = cursor.fetchone()
        if result is None:
            print(f"[skip] character not found: {row['character_name']}")
            continue
        character_id = result[0]
        cursor.execute(
            """
            INSERT INTO character_constellation
            (character_id, constellation, stars)
            VALUES (%s, %s, %s)
            ON CONFLICT (character_id, constellation) DO NOTHING;
            """,
            (character_id, row["constellation"], row["stars"])
        )
    cursor.close()


def main():
    character_df = pd.read_csv(CHARACTER_INFO_PATH)
    tier_df = pd.read_csv(CHARACTER_TIER_PATH)
    constellation_df = pd.read_csv(CHARACTER_CONSTELLATION_PATH)

    conn = connect_db()
    try:
        load_character_data(conn, character_df)
        load_character_tier(conn, tier_df)
        load_character_constellation(conn, constellation_df)
        conn.commit()
        print("Import completed.")
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()