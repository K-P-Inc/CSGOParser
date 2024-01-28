CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS stickers (
    id uuid DEFAULT uuid_generate_v4 (),
    classid TEXT,
    name TEXT,
    key TEXT,
    price FLOAT,
    rare TEXT,
    type TEXT,
    collection TEXT,
    icon_url TEXT,
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX IF NOT EXISTS stickers_index ON stickers(name);

CREATE TYPE csgo_skin_quality AS ENUM (
    'Factory New',
    'Minimal Wear',
    'Field-Tested',
    'Well-Worn',
    'Battle-Scarred'
);

CREATE TABLE IF NOT EXISTS weapons_prices (
  id uuid DEFAULT uuid_generate_v4(),
  name TEXT,
  quality csgo_skin_quality,
  is_stattrak BOOLEAN,
  price FLOAT,
  price_week_low FLOAT,
  price_week_high FLOAT,
  price_month_low FLOAT,
  price_month_high FLOAT,
  price_all_time_low FLOAT,
  price_all_time_high FLOAT,
  parsing_time TIMESTAMP DEFAULT NOW(),
  icon_url TEXT,
  PRIMARY KEY (id)
);

CREATE UNIQUE INDEX IF NOT EXISTS weapons_prices_index ON weapons_prices(name, quality, is_stattrak);

CREATE TYPE weapon_stickers_patern AS ENUM (
    'full-set',
    '3-equal',
    '2-equal',
    'other'
);

CREATE TABLE IF NOT EXISTS skins (
  id uuid DEFAULT uuid_generate_v4 (),
  link TEXT,
  stickers_price FLOAT,
  price FLOAT,
  profit FLOAT,
  skin_id uuid NOT NULL,
  stickers_patern weapon_stickers_patern,
  amount_of_stickers_distinct INTEGER,
  amount_of_stickers INTEGER,
  stickers uuid[],
  in_game_link TEXT,
  FOREIGN KEY (skin_id) REFERENCES weapons_prices (id)
);

CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index ON skins(link);