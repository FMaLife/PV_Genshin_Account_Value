import pandas as pd
import psycopg2

INPUT_PATH = "data/raw/G8_character_info.csv"

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

    cursor = conn.cursor()

    character_df = df.drop_duplicates(subset=["character_name"])

    for _, row in character_df.iterrows():

        cursor.execute(
            """
            INSERT INTO character
            (character_name, rarity, recommended_constellation)
            VALUES (%s, %s, %s);
            """,
            (
                row["character_name"],
                row["rarity"],
                row["recommended_constellation"]
            )
        )

    cursor.close()


def load_character_tier(conn, df):

    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(
            """
            SELECT character_id
            FROM character
            WHERE character_name = %s;
            """,
            (row["character_name"],)
        )

        character_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO character_tier
            (character_id, role, tier)
            VALUES (%s, %s, %s);
            """,
            (
                character_id,
                row["role"],
                row["tier"]
            )
        )

    cursor.close()


def main():

    df = pd.read_csv(INPUT_PATH)

    conn = connect_db()

    try:

        load_character_data(conn, df)
        load_character_tier(conn, df)

        conn.commit()

        print("Import completed.")

    except Exception as e:

        conn.rollback()
        print(e)

    finally:

        conn.close()


if __name__ == "__main__":
    main()