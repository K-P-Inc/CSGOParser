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
  rare TEXT,
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
    'gamerpay',
    'waxpeer'
);

CREATE TABLE IF NOT EXISTS skins (
  id uuid DEFAULT uuid_generate_v4 (),
  link text null,
  parser_type text null,
  stickers_price double precision null,
  price double precision null,
  profit double precision null,
  profit_buff double precision null,
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
  stickers_overprice double precision null,
  FOREIGN KEY (skin_id) REFERENCES weapons_prices (id)
) PARTITION BY LIST (is_sold);

CREATE TABLE skins_sold PARTITION OF skins
  FOR VALUES IN (TRUE);

CREATE TABLE skins_available PARTITION OF skins
  FOR VALUES IN (FALSE)
  PARTITION BY LIST (market);

-- Partition for unsold skins on 'market-csgo'
CREATE TABLE skins_market_csgo_unsold PARTITION OF skins_available
  FOR VALUES IN ('market-csgo');

-- Partition for unsold skins on 'skinbid'
CREATE TABLE skins_skinbid_unsold PARTITION OF skins_available
  FOR VALUES IN ('skinbid');

-- Partition for unsold skins on 'cs-money'
CREATE TABLE skins_cs_money_unsold PARTITION OF skins_available
  FOR VALUES IN ('cs-money');

-- Partition for unsold skins on 'skinport'
CREATE TABLE skins_skinport_unsold PARTITION OF skins_available
  FOR VALUES IN ('skinport');

-- Partition for unsold skins on 'csfloat'
CREATE TABLE skins_csfloat_unsold PARTITION OF skins_available
  FOR VALUES IN ('csfloat');

-- Partition for unsold skins on 'bitskins'
CREATE TABLE skins_bitskins_unsold PARTITION OF skins_available
  FOR VALUES IN ('bitskins');

-- Partition for unsold skins on 'dmarket'
CREATE TABLE skins_dmarket_unsold PARTITION OF skins_available
  FOR VALUES IN ('dmarket');

-- Partition for unsold skins on 'skinbaron'
CREATE TABLE skins_skinbaron_unsold PARTITION OF skins_available
  FOR VALUES IN ('skinbaron');

-- Partition for unsold skins on 'haloskins'
CREATE TABLE skins_haloskins_unsold PARTITION OF skins_available
  FOR VALUES IN ('haloskins');

-- Partition for unsold skins on 'csmiddler'
CREATE TABLE skins_csmiddler_unsold PARTITION OF skins_available
  FOR VALUES IN ('csmiddler');

-- Partition for unsold skins on 'white-market'
CREATE TABLE skins_white_market_unsold PARTITION OF skins_available
  FOR VALUES IN ('white-market');

-- Partition for unsold skins on 'gamerpay'
CREATE TABLE skins_gamerpay_unsold PARTITION OF skins_available
  FOR VALUES IN ('gamerpay');

-- Partition for unsold skins on 'waxpeer'
CREATE TABLE skins_waxpeer_unsold PARTITION OF skins_available
  FOR VALUES IN ('waxpeer');

CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index ON skins(link, is_sold, market);
CREATE INDEX IF NOT EXISTS skins_idx_market ON skins(market);
CREATE INDEX IF NOT EXISTS skins_idx_price ON skins(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at ON skins(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants ON skins USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit ON skins(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff ON skins(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern ON skins(stickers_patern);

-- For 'market-csgo' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_market_csgo ON skins_market_csgo_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_market_csgo ON skins_market_csgo_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_market_csgo ON skins_market_csgo_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_market_csgo ON skins_market_csgo_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_market_csgo ON skins_market_csgo_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_market_csgo ON skins_market_csgo_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_market_csgo ON skins_market_csgo_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_market_csgo ON skins_market_csgo_unsold(stickers_patern);

-- For 'skinbid' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_skinbid ON skins_skinbid_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_skinbid ON skins_skinbid_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_skinbid ON skins_skinbid_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_skinbid ON skins_skinbid_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_skinbid ON skins_skinbid_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_skinbid ON skins_skinbid_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_skinbid ON skins_skinbid_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_skinbid ON skins_skinbid_unsold(stickers_patern);

-- For 'cs-money' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_cs_money ON skins_cs_money_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_cs_money ON skins_cs_money_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_cs_money ON skins_cs_money_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_cs_money ON skins_cs_money_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_cs_money ON skins_cs_money_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_cs_money ON skins_cs_money_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_cs_money ON skins_cs_money_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_cs_money ON skins_cs_money_unsold(stickers_patern);

-- For 'skinport' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_skinport ON skins_skinport_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_skinport ON skins_skinport_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_skinport ON skins_skinport_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_skinport ON skins_skinport_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_skinport ON skins_skinport_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_skinport ON skins_skinport_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_skinport ON skins_skinport_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_skinport ON skins_skinport_unsold(stickers_patern);

-- For 'csfloat' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_csfloat ON skins_csfloat_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_csfloat ON skins_csfloat_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_csfloat ON skins_csfloat_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_csfloat ON skins_csfloat_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_csfloat ON skins_csfloat_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_csfloat ON skins_csfloat_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_csfloat ON skins_csfloat_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_csfloat ON skins_csfloat_unsold(stickers_patern);

-- For 'bitskins' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_bitskins ON skins_bitskins_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_bitskins ON skins_bitskins_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_bitskins ON skins_bitskins_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_bitskins ON skins_bitskins_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_bitskins ON skins_bitskins_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_bitskins ON skins_bitskins_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_bitskins ON skins_bitskins_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_bitskins ON skins_bitskins_unsold(stickers_patern);

-- For 'dmarket' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_dmarket ON skins_dmarket_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_dmarket ON skins_dmarket_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_dmarket ON skins_dmarket_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_dmarket ON skins_dmarket_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_dmarket ON skins_dmarket_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_dmarket ON skins_dmarket_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_dmarket ON skins_dmarket_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_dmarket ON skins_dmarket_unsold(stickers_patern);

-- For 'skinbaron' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_skinbaron ON skins_skinbaron_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_skinbaron ON skins_skinbaron_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_skinbaron ON skins_skinbaron_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_skinbaron ON skins_skinbaron_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_skinbaron ON skins_skinbaron_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_skinbaron ON skins_skinbaron_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_skinbaron ON skins_skinbaron_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_skinbaron ON skins_skinbaron_unsold(stickers_patern);

-- For 'haloskins' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_haloskins ON skins_haloskins_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_haloskins ON skins_haloskins_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_haloskins ON skins_haloskins_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_haloskins ON skins_haloskins_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_haloskins ON skins_haloskins_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_haloskins ON skins_haloskins_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_haloskins ON skins_haloskins_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_haloskins ON skins_haloskins_unsold(stickers_patern);

-- For 'csmiddler' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_csmiddler ON skins_csmiddler_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_csmiddler ON skins_csmiddler_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_csmiddler ON skins_csmiddler_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_csmiddler ON skins_csmiddler_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_csmiddler ON skins_csmiddler_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_csmiddler ON skins_csmiddler_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_csmiddler ON skins_csmiddler_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_csmiddler ON skins_csmiddler_unsold(stickers_patern);

-- For 'white-market' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_white_market ON skins_white_market_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_white_market ON skins_white_market_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_white_market ON skins_white_market_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_white_market ON skins_white_market_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_white_market ON skins_white_market_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_white_market ON skins_white_market_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_white_market ON skins_white_market_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_white_market ON skins_white_market_unsold(stickers_patern);

-- For 'gamerpay' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_gamerpay ON skins_gamerpay_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_gamerpay ON skins_gamerpay_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_gamerpay ON skins_gamerpay_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_gamerpay ON skins_gamerpay_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_gamerpay ON skins_gamerpay_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_gamerpay ON skins_gamerpay_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_gamerpay ON skins_gamerpay_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_gamerpay ON skins_gamerpay_unsold(stickers_patern);

-- For 'waxpeer' partition
CREATE UNIQUE INDEX IF NOT EXISTS skins_link_index_waxpeer ON skins_waxpeer_unsold(link);
CREATE INDEX IF NOT EXISTS skins_idx_market_waxpeer ON skins_waxpeer_unsold(market);
CREATE INDEX IF NOT EXISTS skins_idx_price_waxpeer ON skins_waxpeer_unsold(price);
CREATE INDEX IF NOT EXISTS skins_idx_created_at_waxpeer ON skins_waxpeer_unsold(created_at);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_distinct_variants_waxpeer ON skins_waxpeer_unsold USING gin(stickers_distinct_variants);
CREATE INDEX IF NOT EXISTS skins_idx_profit_waxpeer ON skins_waxpeer_unsold(profit);
CREATE INDEX IF NOT EXISTS skins_idx_profit_buff_waxpeer ON skins_waxpeer_unsold(profit_buff);
CREATE INDEX IF NOT EXISTS skins_idx_stickers_patern_waxpeer ON skins_waxpeer_unsold(stickers_patern);
