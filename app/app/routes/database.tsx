import React, { useEffect, useRef, useState } from 'react';
import type { LoaderFunctionArgs } from "@remix-run/node";
import { Form, defer, useLoaderData, useOutletContext, useSubmit, Await, useFetcher } from "@remix-run/react";
import ItemCard from "~/components/shared/ItemCard";
import { RDSClient } from "~/models/postgres.server";
import { OutletContext, SkinItem } from "~/types";
import { Switch } from "~/components/ui/switch";
import { Label } from "~/components/ui/label";
import { Button } from "~/components/ui/button";
import SkeletonItemCard from '~/components/shared/SkeletonItemCard';
import { MarketFilter } from '~/components/shared/MarketFilter';
import { WearType, StickersPattern, StickersType, WeaponType, ShopType, SortType, CategoryType } from "~/types";
import { FrownOutlined } from '@ant-design/icons';
import Cookies from 'universal-cookie';

const MAX_PAGE_ITEMS = 100;

const InfiniteScroller = (props: { children: any; loading: boolean; loadNext: () => void; }) => {
  const { children, loading, loadNext } = props;
  const scrollListener = useRef(loadNext);
  const isLoadingRef = useRef(loading);

  useEffect(() => {
    scrollListener.current = loadNext;
  }, [loadNext]);

  useEffect(() => {
    isLoadingRef.current = loading;
  }, [loading])

  const onScroll = (e: any) => {
    const div = e.target;
    const scrollDifference = Math.floor(div.scrollHeight - div.scrollTop - div.clientHeight);
    const scrollEnded = scrollDifference - 1000 <= 0;
    if (scrollEnded && !isLoadingRef.current) {
      scrollListener.current();
    }
  };

  useEffect(() => {
    if (typeof window !== "undefined") {
      const cls = document.getElementsByClassName("home-container");
      if (cls.length > 0) {
        const div = cls[0] as HTMLDivElement;
        div.addEventListener("scroll", onScroll);
      }
    }
    return () => {
      const cls = document.getElementsByClassName("home-container");
      if (cls.length > 0) {
        const div = cls[0] as HTMLDivElement;
        div.removeEventListener("scroll", onScroll);
      }
    };
  }, []);

  return <>{children}</>;
}

function getParamArray<T>(url: string, param: string): T[] {
  const urlStruct = new URL(url);
  const paramValue = urlStruct.searchParams.get(param);
  return paramValue ? paramValue.split(",").map(type => type as T) : [];
}

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  const sort_by: SortType | undefined = url.searchParams.get("sort_by") ? url.searchParams.get("sort_by") as SortType : undefined;
  const search: string = url.searchParams.get("search") ?? "";
  const weapon_types = getParamArray<WeaponType>(request.url, "weapon_types");
  const wears = getParamArray<WearType>(request.url, "wears");
  const categories = getParamArray<CategoryType>(request.url, "categories");
  const min_price: number | undefined = url.searchParams.get("min_price") ? parseFloat(url.searchParams.get("min_price") ?? "") : undefined;
  const max_price: number | undefined = url.searchParams.get("max_price") ? parseFloat(url.searchParams.get("max_price") ?? "") : undefined;
  const stickers_patterns = getParamArray<StickersPattern>(request.url, "stickers_patterns");
  const sticker_types = getParamArray<StickersType>(request.url, "sticker_types");
  const market_types = getParamArray<ShopType>(request.url, "market_types");
  const profit_based: string = url.searchParams.get("profit_based") ?? "steam";
  const direct_item_id: string | null = url.searchParams.get("direct_item_id");
  const only_liked_items: boolean = url.searchParams.get("only_liked_items") ? true : false;
  const page = parseInt(url.searchParams.get("page") || "0");
  const cookieHeader = request.headers?.get("Cookie");
  const cookies = new Cookies(cookieHeader);
  const likedItemsArray = cookies.get("liked_items") ? cookies.get("liked_items").split(",") : [];

  let stickers_filters = [];
  let filters = [`skins.stickers_price > 5`, `skins.order_type = 'fixed'`, `weapons_prices.price > 1`];
  let args = [];

  if (only_liked_items) {
    if (likedItemsArray.length > 0) {
      filters.push(likedItemsArray.map((item: string, index: number) => `skins.id = $${index + 1}`).join(` OR `));
      likedItemsArray.forEach((item: string) => args.push(item));
    } else {
      filters.push(`skins.id = null`);
    }
  } else {
    if (categories.length > 0) {
      const categories_filters = {
        "StatTrak™": `weapons_prices.is_stattrak = TRUE`,
        "Normal": `weapons_prices.is_stattrak = FALSE`
      };
      filters.push(categories.map(category => categories_filters[category]).join(` OR `));
    }
    if (wears.length > 0) {
      filters.push(wears.map(quality => `weapons_prices.quality = '${quality}'`).join(` OR `));
    }
    if (weapon_types.length > 0) {
      filters.push(weapon_types.map(weapon_type => `LOWER(weapons_prices.name) LIKE LOWER('${weapon_type}%')`).join(` OR `));
    }
    if (stickers_patterns.length > 0) {
      filters.push(stickers_patterns.map(stickers_patern => `skins.stickers_patern = '${stickers_patern}'`).join(` OR `));
    }

    if (sticker_types.length > 0) {
      filters.push(`skins.stickers_distinct_variants <@ ARRAY[${sticker_types.map(value => `'${value}'`).join(`,`)}]::csgo_stickers_variant[]`)
    }

    if (search.length > 0) {
      filters.push(`LOWER(weapons_prices.name) LIKE LOWER($1)`)
      args.push(`%${search}%`)
    }
    if (min_price !== undefined) {
      filters.push(`skins.price >= ${min_price}`)
    }
    if (max_price !== undefined) {
      filters.push(`skins.price <= ${max_price}`)
    }

    if (direct_item_id !== null) {
      filters.push(`skins.id != $${args.length + 1}`)
      args.push(direct_item_id)
    }

    if (market_types.length > 0) {
      const market_keys = {
        "bitskins.com": "bitskins",
        "cs.money": "cs-money",
        "csfloat.com": "csfloat",
        "dmarket.com": "dmarket",
        "haloskins.com": "haloskins",
        "market.csgo.com": "market-csgo",
        "skinbid.com": "skinbid",
        "skinport.com": "skinport",
        "white.market": "white-market",
        "skinbaron.de": "skinbaron",
        "gamerpay.gg": 'gamerpay',
        "waxpeer.com": 'waxpeer'
      }

      filters.push(
        market_types
          .map((market_type: ShopType) => `skins.market = '${market_keys[market_type as keyof typeof market_keys]}'`)
          .join(' OR ')
      );
    }
  }

  filters.push(`skins.is_sold = FALSE`);

  const filterCondition = filters.length ? `WHERE ${filters.map(value => `(${value})`).join(' AND ')}` : '';

  let orderBy = '';
  switch (sort_by) {
    case 'newest':
      orderBy = 'ORDER BY created_at DESC';
      break;
    case 'oldest':
      orderBy = 'ORDER BY created_at ASC';
      break;
    case 'profit_high_to_low':
      orderBy = `ORDER BY ${profit_based === 'buff' ? `profit_buff` : `profit`} DESC`;
      break;
    case 'profit_low_to_high':
      orderBy = `ORDER BY ${profit_based === 'buff' ? `profit_buff` : `profit`} ASC`;
      break;
    case 'price_high_to_low':
      orderBy = 'ORDER BY market_price DESC';
      break;
    case 'price_low_to_high':
      orderBy = 'ORDER BY market_price ASC';
      break;
    default:
      orderBy = '';
  }

  const query = `
    SELECT
      skins.id,
      weapons_prices.name,
      skins.market,
      skins.stickers_distinct_variants,
      skins.stickers_wears,
      skins.order_type,
      skins.item_float,
      skins.pattern_template,
      skins.in_game_link,
      weapons_prices.is_stattrak,
      weapons_prices.quality,
      skins.price AS market_price,
      weapons_prices.price AS steam_price,
      weapons_prices.icon_url,
      skins.stickers_patern,
      skins.created_at,
      skins.stickers_price,
      skins.link,
      skins.stickers,
      skins.stickers_overprice,
      ${profit_based === 'buff' ? `skins.profit_buff` : `skins.profit`}
    FROM skins
    INNER JOIN weapons_prices ON skins.skin_id = weapons_prices.id
    ${filterCondition}
    ${orderBy}
    LIMIT ${MAX_PAGE_ITEMS} OFFSET ${page * MAX_PAGE_ITEMS};
  `;

  const directQuery = `
    SELECT
      skins.id,
      weapons_prices.name,
      skins.market,
      skins.stickers_distinct_variants,
      skins.stickers_wears,
      skins.order_type,
      skins.item_float,
      skins.pattern_template,
      skins.in_game_link,
      weapons_prices.is_stattrak,
      weapons_prices.quality,
      skins.price AS market_price,
      weapons_prices.price AS steam_price,
      weapons_prices.icon_url,
      skins.stickers_patern,
      skins.created_at,
      skins.stickers_price,
      skins.link,
      skins.stickers,
      skins.stickers_overprice,
      ${profit_based === 'buff' ? `skins.profit_buff` : `skins.profit`}
    FROM skins
    INNER JOIN weapons_prices ON skins.skin_id = weapons_prices.id
    WHERE skins.id = $1
    LIMIT 1
  `

  let promises = {
    items: (new RDSClient()).query(query, args),
    stickers: (new RDSClient()).query('SELECT * FROM stickers'),
    directItem: direct_item_id ? (new RDSClient()).query(directQuery, [direct_item_id]) : Promise.resolve(null)
  }

  let filtered_items: Promise<SkinItem[]> = Promise.all(Object.values(promises))
    .then(async (responses: any[]) => {

      const [items, stickersMap, directItem] = responses

      const filteredItems = items
        ? (directItem && page === 0 ? [...directItem, ...items] : items).map((row: any) => ({
          id: row["id"],
          name: `${row["is_stattrak"] ? "StatTrak™ " : ""}${row["name"]}`,
          market: row["market"],
          type: `${row["name"].split(" ")[0]}`,
          is_stattrak: row["is_stattrak"],
          quality: `${row["quality"]}`,
          market_price: row["market_price"],
          steam_price: row["steam_price"] * (profit_based === 'buff' ? 0.65 : 1),
          stickers_patern: row["stickers_patern"],
          stickers_overprice: row["stickers_overprice"],
          image: row["icon_url"].startsWith("https://steamcommunity-a.akamaihd.net/economy/image/-") ? row["icon_url"] : `https://community.akamai.steamstatic.com/economy/image/${row["icon_url"]}`,
          profit: row[profit_based === 'buff' ? `profit_buff` : "profit"],
          link: `${row["link"]}`,
          stickers_instances: stickersMap.filter((x: any) => row["stickers"].includes(x["id"])),
          stickers_icons: row["stickers"].map((stc: string) => {
            const stc_instance = stickersMap.find((ins: any) => ins["id"] === stc)
            return `https://community.akamai.steamstatic.com/economy/image/${stc_instance["icon_url"]}`
          }),
          stickers_price: row["stickers"].map((stc: string) => {
            const stc_instance = stickersMap.find((ins: any) => ins["id"] === stc)
            return stc_instance["price"];
          }).reduce((accumulator: number, currentValue: number) => accumulator + currentValue, 0),
          stickers_wears: row["stickers_wears"],
          order_type: row["order_type"],
          item_float: row["item_float"],
          pattern_template: row["pattern_template"],
          in_game_link: row["in_game_link"],
          profit_based_on: profit_based
        }))
        : []

      return filteredItems;
    });

  return defer({
    items: filtered_items,
    weapon_types: weapon_types,
    sort_by: sort_by,
    search: search,
    categories: categories,
    min_price: min_price,
    max_price: max_price,
    stickers_patterns: stickers_patterns,
    sticker_types: sticker_types,
    market_types: market_types,
    wears: wears,
    profit_based: profit_based,
    page: page,
    direct_item_id: direct_item_id,
    only_liked_items: only_liked_items
  });
}

export default function Index() {
  const submit = useSubmit();
  const {
    items, weapon_types, sort_by, search, categories,
    min_price, max_price, stickers_patterns, sticker_types,
    market_types, wears, profit_based, page, direct_item_id,
    only_liked_items
  } = useLoaderData<typeof loader>();
  const [skins, setSkins] = useState<SkinItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const fetcher = useFetcher<typeof loader>();
  const pageRef = useRef(page);
  const skinsRef = useRef<SkinItem[]>([]);

  const preloadImages = (newItems: SkinItem[]) => {
    let imageLinks = new Set<string>();

    newItems.forEach((item: SkinItem) => {
      if (item.image) {
        imageLinks.add(item.image);
      }
      if (item.stickers_icons) {
        item.stickers_icons.forEach((icon: string) => imageLinks.add(icon));
      }
    });

    imageLinks.forEach((src: string) => {
      var img: HTMLImageElement = new Image();
      img.src = src;
    });
  }

  const addNewSkins = (newItems: SkinItem[]) => {
    preloadImages(newItems);
    setSkins((prevSkins) => {
      skinsRef.current = [...prevSkins, ...newItems]

      return skinsRef.current
    });
    setIsLoading(false);
  }

  useEffect(() => {
    const updateSkins = async () => {
      if (!fetcher.data || fetcher.state === "loading") {
        return;
      }
      if (fetcher.data) {
        const newItems = await fetcher.data.items;
        addNewSkins(newItems);
      }
    };

    updateSkins();
  }, [fetcher.data?.items]);

  useEffect(() => {
    const updateSkins = async () => {
      const newSkins = await items;
      preloadImages(newSkins);
      skinsRef.current = newSkins;
      setSkins(newSkins);
      setIsLoading(false);
    };

    updateSkins();
  }, [items]);

  return (
    <div className="flex flex-1">
      <div className="home-container">
        <div className="home-posts h-full">
          <h1 className="h3-bold md:h2-bold text-left w-full">Markets items</h1>
          <MarketFilter
            submit={(target: any) => {
              submit(target, { replace: true });
              setSkins([]);
              setIsLoading(true);
            }}
            only_liked_items={only_liked_items}
            wears={wears as WearType[]}
            weapons={weapon_types as WeaponType[]}
            shops={market_types as ShopType[]}
            search={search}
            categories={categories}
            stickersPatterns={stickers_patterns as StickersPattern[]}
            stickersTypes={sticker_types as StickersType[]}
            min_price={min_price}
            max_price={max_price}
            sort_by={sort_by}
            profit_based={profit_based}
          />
          <InfiniteScroller
            loadNext={() => {
              if (isLoading || skinsRef.current.length % MAX_PAGE_ITEMS !== 0) { return };
              setIsLoading(true);
              const newPage = pageRef.current + 1;
              pageRef.current = newPage;

              const query = new URLSearchParams(window.location.search);
              query.set("page", newPage.toString());

              fetcher.load(`?${query.toString()}`);
            }}
            loading={isLoading}
          >
            <div className="gap-2 w-full justify-items-center inline-grid" style={(!isLoading && skins.length === 0) ? { height: "100%"} : { gridTemplateColumns: "repeat(auto-fill, minmax(210px, 1fr))", display: "grid" }}>
              {skins.map((item: SkinItem) => (
                <ItemCard item={item} key={item.link} defaultOpen={direct_item_id === item.id}/>
              ))}
              {isLoading &&
                [...Array(MAX_PAGE_ITEMS).keys()].map((i) => <div className="w-full" key={i}><SkeletonItemCard/></div>)
              }
              {!isLoading && skins.length === 0 && (
                <div className="flex h-full w-full items-center justify-center text-center">
                  <div className='space-y-6'>
                    <FrownOutlined className='text-primary-500 text-4xl' />
                    <div>
                      <h3 className="text-2xl font-bold text-light-1 mb-2">Nothing was found</h3>
                      <p className='text-light-3'>Try to reset filters or change search request</p>
                    </div>
                    <Button
                      onClick={() => {
                        submit({}, { replace: true });
                        setSkins([]);
                        setIsLoading(true);
                      }}
                      variant={"primary"}
                    >
                      Clear all filters
                    </Button>
                  </div>
                </div>
              )}
            </div>
          </InfiniteScroller>
        </div>
      </div>
    </div>
  );
}
