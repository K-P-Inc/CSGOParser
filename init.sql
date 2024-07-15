CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS stickers (
    id uuid DEFAULT uuid_generate_v4 (),
    classid TEXT,
    name TEXT,
    key TEXT,
    price FLOAT,
    market_prices JSON,
    price_week_low FLOAT,
    price_week_high FLOAT,
    price_month_low FLOAT,
    price_month_high FLOAT,
    price_all_time_low FLOAT,
    price_all_time_high FLOAT,
    rare TEXT,
    type TEXT,
    collection TEXT,
    parsing_time TIMESTAMP DEFAULT NOW(),
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

CREATE TYPE csgo_stickers_variant AS ENUM (
    'Paper',
    'Glitter',
    'Holo',
    'Foil',
    'Gold'
);

CREATE TABLE IF NOT EXISTS weapons_prices (
  id uuid DEFAULT uuid_generate_v4(),
  name TEXT,
  quality csgo_skin_quality,
  is_stattrak BOOLEAN,
  price FLOAT,
  market_prices JSON,
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
    '5-equal',
    '4-equal',
    '3-equal',
    '2-equal',
    'other'
);

CREATE TYPE csgo_order_type AS ENUM (
    'auction',
    'fixed'
);

CREATE TYPE market_type AS ENUM (
    'market-csgo',
    'skinbid',
    'cs-money',
    'skinport',
    'csfloat',
    'bitskins',
    'dmarket',
    'skinbaron',
    'haloskins',
    'csmiddler',
    'white-market',
    'gamerpay'
);

CREATE TABLE IF NOT EXISTS skins (
  id uuid DEFAULT uuid_generate_v4 (),
  link text null,
  stickers_price double precision null,
  price double precision null,
  profit double precision null,
  skin_id uuid not null,
  stickers_patern public.weapon_stickers_patern null,
  amount_of_stickers_distinct integer null,
  amount_of_stickers integer null,
  stickers uuid[] default ARRAY[]::uuid[],
  stickers_wears double precision[] default ARRAY[]::double precision[],
  order_type csgo_order_type default 'fixed'::csgo_order_type,
  stickers_distinct_variants csgo_stickers_variant[] default ARRAY[]::csgo_stickers_variant[],
  item_float double precision null,
  pattern_template double precision null,
  created_at timestamp with time zone null default now(),
  is_out_dated boolean null default false,
  in_game_link text null default ''::text,
  is_sold boolean not null default false,
  is_deleted boolean null default false,
  market market_type null,
  FOREIGN KEY (skin_id) REFERENCES weapons_prices (id)
);

CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index ON skins(link);
CREATE INDEX IF NOT EXISTS skins_idx_market ON skins(market);
CREATE INDEX IF NOT EXISTS skins_idx_price ON skins(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at ON skins(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants ON skins USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit ON skins(profit);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern ON skins(stickers_patern);
