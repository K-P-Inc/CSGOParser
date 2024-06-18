import type { LoaderFunctionArgs } from "@remix-run/node";
import { Form, json, useActionData, useFetcher, useLoaderData, useOutletContext, useSubmit } from "@remix-run/react";
import ItemCard from "~/components/shared/ItemCard";
import { RDSClient } from "~/models/postgres.server";
import { OutletContext, SkinItem } from "~/types";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select"
import { Switch } from "~/components/ui/switch";
import { Label } from "~/components/ui/label";
import { useEffect, useRef, useState } from "react";
import { createSupabaseServerClient } from "~/supabase.server";
import { Button } from "~/components/ui/button";

const MAX_PAGE_ITEMS = 60;

const InfiniteScroller = (props: {
  children: any;
  loading: boolean;
  loadNext: () => void;
}) => {
  const { children, loading, loadNext } = props;
  const scrollListener = useRef(loadNext);

  useEffect(() => {
    scrollListener.current = loadNext;
  }, [loadNext]);

  const onScroll = (e: any) => {
    const div = e.target;
    const scrollDifference = Math.floor(div.scrollHeight - div.scrollTop - div.clientHeight);
    const scrollEnded = scrollDifference === 0;
    if (scrollEnded && !loading) {
      scrollListener.current();
    }
  };

  useEffect(() => {
    if (typeof window !== "undefined") {
      console.log("added listener");
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

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const url = new URL(request.url);
  const is_stattrak = url.searchParams.get("is_stattrak");
  const weapon_type = url.searchParams.get("weapon_type");
  const sort_by = url.searchParams.get("sort_by");
  const stickers_patern = url.searchParams.get("stickers_patern");
  const market_type = url.searchParams.get("market_type");
  const page = parseInt(url.searchParams.get("page") || "0");
  const postgresClient = new RDSClient();

  const filters = [];
  if (is_stattrak === "on") {
    filters.push(`weapons_prices.is_stattrak = TRUE`);
  }
  if (weapon_type) {
    filters.push(`LOWER(weapons_prices.name) LIKE LOWER('%${weapon_type}%')`);
  }
  if (stickers_patern) {
    filters.push(`skins.stickers_patern = '${stickers_patern}'`);
  }
  if (market_type) {
    filters.push(`skins.market = '${market_type}'`);
  }
  filters.push(`(COALESCE(stickers_total_price, 0) * 0.1 + weapons_prices.price - skins.price) / skins.price * 100.0 > 10`);
  filters.push(`skins.is_sold = FALSE`);

  const filterCondition = filters.length ? `WHERE ${filters.join(' AND ')}` : '';

  // Construct the sorting
  let orderBy = '';
  switch (sort_by) {
    case 'profit_high_to_low':
      orderBy = 'ORDER BY profit DESC';
      break;
    case 'profit_low_to_high':
      orderBy = 'ORDER BY profit ASC';
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
  SELECT * FROM (
      WITH sticker_prices AS (
        SELECT
          skins.id AS skin_id,
          SUM(COALESCE(stickers.price, 0)) AS stickers_total_price
        FROM skins
        LEFT JOIN stickers ON stickers.id = ANY(skins.stickers)
        GROUP BY skins.id
      )
      SELECT DISTINCT ON (skins.id)
        weapons_prices.name,
        skins.market,
        weapons_prices.is_stattrak,
        weapons_prices.quality,
        skins.price AS market_price,
        weapons_prices.price AS steam_price,
        weapons_prices.icon_url,
        COALESCE(sticker_prices.stickers_total_price, 0) AS stickers_price,
        skins.stickers_patern,
        skins.link,
        skins.stickers,
        array_to_json(array_agg(row_to_json(t)) OVER (PARTITION BY skins.id)) AS stickers_array,
        (COALESCE(sticker_prices.stickers_total_price, 0) * 0.1 + weapons_prices.price - skins.price) / skins.price * 100.0 AS profit
      FROM skins
      INNER JOIN weapons_prices ON skins.skin_id = weapons_prices.id
      LEFT JOIN sticker_prices ON skins.id = sticker_prices.skin_id
      LEFT JOIN stickers t ON t.id = ANY (skins.stickers)
      ${filterCondition}
    )
    ${orderBy}
    LIMIT ${MAX_PAGE_ITEMS} OFFSET ${page * MAX_PAGE_ITEMS};
  `;

  let items = await postgresClient.query(query);

  const filtered_items: SkinItem[] | [] = items
    ? items.map((row: any) => ({
        name: `${row["is_stattrak"] ? "StatTrak™ " : ""}${row["name"]}`,
        market: row["market"],
        type: `${row["name"].split(" ")[0]}`,
        is_stattrak: row["is_stattrak"],
        quality: `${row["quality"]}`,
        market_price: row["market_price"],
        steam_price: row["steam_price"],
        stickers_patern: row["stickers_patern"],
        image: `https://community.akamai.steamstatic.com/economy/image/${row["icon_url"]}`,
        profit: row["profit"],
        link: `${row["link"]}`,
        stickers_instances: row["stickers_array"],
        stickers_icons: row["stickers"].map((stc: string) => {
          const stc_instance = row["stickers_array"].find((ins: any) => ins["id"] === stc)
          return `https://community.akamai.steamstatic.com/economy/image/${stc_instance["icon_url"]}`
        }),
        stickers_price: row["stickers"].map((stc: string) => {
          const stc_instance = row["stickers_array"].find((ins: any) => ins["id"] === stc)
          return stc_instance["price"];
        }).reduce((accumulator: number, currentValue: number) => accumulator + currentValue, 0)
      }))
    : [];

  return json({
    items: filtered_items,
    is_stattrak: is_stattrak !== null,
    weapon_type: weapon_type,
    sort_by: sort_by,
    stickers_patern: stickers_patern,
    market_type: market_type,
    page: page
  });
}

export default function Index() {
  const submit = useSubmit();
  const { session } = useOutletContext<OutletContext>();
  const { items, is_stattrak, weapon_type, sort_by, stickers_patern, market_type, page } = useLoaderData<typeof loader>();
  const fetcher = useFetcher<typeof loader>();
  const [skins, setSkins] = useState<SkinItem[]>(items);
  const formRef = useRef<HTMLFormElement>(null);

  const handleSubmit = (
    { sort_by, weapon_type, is_stattrak, stickers_patern, market_type } :
    { sort_by?: string, weapon_type?: string, is_stattrak?: boolean, stickers_patern?: string, market_type?: string }
  ) => {
    const formData = new FormData(formRef.current ?? undefined)

    if (sort_by) {
      formData.set("sort_by", sort_by)
    }
    if (weapon_type) {
      formData.set("weapon_type", weapon_type)
    }
    if (market_type) {
      formData.set("market_type", market_type)
    }
    if (stickers_patern) {
      formData.set("stickers_patern", stickers_patern)
    }
    if (is_stattrak == true) {
      formData.set("is_stattrak", "on")
    } else if (is_stattrak == false) {
      formData.delete("is_stattrak")
    }

    submit(formData, { replace: true });
  }

  // An effect for appending data to items state
  useEffect(() => {
    if (!fetcher.data || fetcher.state === "loading") {
      return;
    }
    // If we have new data - append it
    if (fetcher.data) {
      const newItems = fetcher.data.items;
      console.log("Appending data", newItems.length);
      setSkins((prevAssets) => [...prevAssets, ...newItems]);
    }
  }, [fetcher.data]);

  useEffect(() => {
    setSkins(items);
  }, [items])

  return (
    <div className="flex flex-1">
      <div className="home-container">
        <div className="home-posts">
          <h2 className="h3-bold md:h2-bold text-left w-full">Inventory items</h2>
          <Form ref={formRef} method="get" className="flex flex-1 w-full items-center gap-x-5">
            <Select name="sort_by" value={sort_by ?? undefined} onValueChange={(value: string) => handleSubmit({ sort_by: value })}>
              <SelectTrigger className="max-w-[180px]">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Types</SelectLabel>
                  <SelectItem value="profit_high_to_low">Profit: High to Low</SelectItem>
                  <SelectItem value="profit_low_to_high">Profit: Low to High</SelectItem>
                  <SelectItem value="price_high_to_low">Price: High to Low</SelectItem>
                  <SelectItem value="price_low_to_high">Price: Low to High</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <Select name="weapon_type" value={weapon_type?.toUpperCase() ?? undefined} onValueChange={(value: string) => handleSubmit({ weapon_type: value })}>
              <SelectTrigger className="max-w-[180px]">
                <SelectValue placeholder="Weapon type"/>
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Types</SelectLabel>
                  {["AWP", "AK-47", "M4A1-S", "M4A4"].map((item: string) => <SelectItem key={item} value={item}>{item}</SelectItem>)}
                </SelectGroup>
              </SelectContent>
            </Select>
            <Select name="stickers_patern" value={stickers_patern ?? undefined} onValueChange={(value: string) => handleSubmit({ stickers_patern: value })}>
              <SelectTrigger className="max-w-[180px]">
                <SelectValue placeholder="Stickers' pattern" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Types</SelectLabel>
                  <SelectItem value="5-equal">5 equal</SelectItem>
                  <SelectItem value="4-equal">4 equal</SelectItem>
                  <SelectItem value="3-equal">3 equal</SelectItem>
                  <SelectItem value="2-equal">2 equal</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <Select name="market_type" value={market_type ?? undefined} onValueChange={(value: string) => handleSubmit({ market_type: value })}>
              <SelectTrigger className="max-w-[180px]">
                <SelectValue placeholder="Market type" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Market</SelectLabel>
                  <SelectItem value="bitskins">bitskins.com</SelectItem>
                  <SelectItem value="cs-money">cs.money</SelectItem>
                  <SelectItem value="csfloat">csfloat.com</SelectItem>
                  <SelectItem value="dmarket">dmarket.com</SelectItem>
                  <SelectItem value="haloskins">haloskins.com</SelectItem>
                  <SelectItem value="market-csgo">market.csgo.com</SelectItem>
                  <SelectItem value="skinbid">skinbid.com</SelectItem>
                  <SelectItem value="skinport">skinport.com</SelectItem>
                  <SelectItem value="white-market">white.market</SelectItem>
                  <SelectItem value="skinbaron">skinbaron.de</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <div className="flex items-center space-x-2">
              <Switch name="is_stattrak" checked={is_stattrak} onCheckedChange={(checked: boolean) => handleSubmit({ is_stattrak: checked })}/>
              <Label htmlFor="terms" className="min-w-[100px] base-small">Is StatTrak</Label>
            </div>
          </Form>
          <InfiniteScroller
            loadNext={() => {
              const newPage = fetcher.data
                ? fetcher.data.page + 1
                : page + 1;
              const query = window.location.search
                ? `${window.location.search}&page=${newPage}`
                : `?page=${newPage}`;

              fetcher.load(query);
            }}
            loading={fetcher.state === "loading"}
          >
            <div className="gap-2 w-full justify-items-center inline-grid" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(170px, 1fr))", display: "grid" }}>
              {skins?.map((item: SkinItem) => (
                <ItemCard item={item} key={item.link} />
              ))}
            </div>
          </InfiniteScroller>
        </div>
      </div>
    </div>
  )
}