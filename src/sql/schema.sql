DROP TABLE IF EXISTS character_tier;
DROP TABLE IF EXISTS character;

CREATE TABLE character (
    character_id SERIAL PRIMARY KEY,
    character_name VARCHAR(50) NOT NULL UNIQUE,
    rarity SMALLINT NOT NULL,
    recommended_constellation VARCHAR(2) NOT NULL
);

CREATE TABLE character_tier (
    character_tier_id SERIAL PRIMARY KEY,
    character_id INT NOT NULL,
    role VARCHAR(20) NOT NULL,
    tier VARCHAR(2) NOT NULL,

    CONSTRAINT fk_character
        FOREIGN KEY (character_id)
        REFERENCES character(character_id),

    CONSTRAINT uq_character_role
        UNIQUE (character_id, role)
);