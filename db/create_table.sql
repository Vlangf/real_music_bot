CREATE TABLE IF NOT EXISTS songs
(
    like_            VARCHAR,
    id               serial PRIMARY KEY,
    genre            VARCHAR(255),
    name             VARCHAR(255),
    link             VARCHAR(255),
    band_name        VARCHAR(255),
    date_add_to_site VARCHAR(255)
)