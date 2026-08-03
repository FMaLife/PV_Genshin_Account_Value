DROP TABLE IF EXISTS character_constellation;
DROP TABLE IF EXISTS character_tier;
DROP TABLE IF EXISTS character;

CREATE TABLE character (
    character_id SERIAL PRIMARY KEY,
    character_name VARCHAR(50) NOT NULL UNIQUE,
    rarity SMALLINT NOT NULL
);

CREATE TABLE character_tier (
    character_tier_id SERIAL PRIMARY KEY,
    character_id INT NOT NULL,
    role VARCHAR(20) NOT NULL,
    tier VARCHAR(2) NOT NULL,
    CONSTRAINT fk_character_tier
        FOREIGN KEY (character_id)
        REFERENCES character(character_id),
    CONSTRAINT uq_character_role
        UNIQUE (character_id, role)
);

CREATE TABLE character_constellation (
    character_constellation_id SERIAL PRIMARY KEY,
    character_id INT NOT NULL,
    constellation VARCHAR(2) NOT NULL,
    stars SMALLINT NOT NULL,
    CONSTRAINT fk_character_constellation
        FOREIGN KEY (character_id)
        REFERENCES character(character_id),
    CONSTRAINT uq_character_constellation
        UNIQUE (character_id, constellation)
);