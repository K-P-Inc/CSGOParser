import type { LoaderFunctionArgs } from "@remix-run/node";
import { Form, json, useActionData, useLoaderData, useOutletContext, useSubmit } from "@remix-run/react";
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
import { useRef } from "react";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const rdsClient = new RDSClient();

  const items = await rdsClient.query(
    `
      SELECT distinct on (skins.id)
        weapons_prices.name,
        weapons_prices.is_stattrak,
        weapons_prices.quality,
        skins.price AS market_price,
        weapons_prices.price AS steam_price,
        weapons_prices.icon_url,
        skins.stickers_price,
        skins.stickers_patern,
        skins.profit,
        skins.link,
        skins.stickers,
        array_to_json(array_agg(row_to_json(t)) over ( partition by skins.id )) as stickers_array
      FROM skins
      INNER JOIN weapons_prices ON skins.skin_id = weapons_prices.id
      LEFT JOIN stickers t on t.id = any (skins.stickers)
      WHERE is_sold = FALSE
    `
  );

  const url = new URL(request.url);
  const is_stattrak = url.searchParams.get("is_stattrak");
  const weapon_type = url.searchParams.get("weapon_type");
  const sort_by = url.searchParams.get("sort_by");

  const filtered_items: SkinItem[] | null = items
    ? items.map((row) => ({
        name: `${row["is_stattrak"] ? "StatTrak™ " : ""}${row["name"]}`,
        type: `${row["name"].split(" ")[0]}`,
        is_stattrak: row["is_stattrak"],
        quality: `${row["quality"]}`,
        market_price: row["market_price"],
        steam_price: row["steam_price"],
        stickers_patern: row["stickers_patern"],
        image: `https://community.akamai.steamstatic.com/economy/image/${row["icon_url"]}`,
        stickers_price: row["stickers_price"],
        profit: row["profit"],
        link: `${row["link"]}`,
        stickers_instances: row["stickers_array"],
        stickers_icons: row["stickers"].map((stc: string) => {
          const stc_instance = row["stickers_array"].find((ins: any) => ins["id"] === stc)
          return `https://community.akamai.steamstatic.com/economy/image/${stc_instance["icon_url"]}`
      })
    }))
      .filter((skin: SkinItem) => is_stattrak === "on" ? skin.is_stattrak === true : true)
      .filter((skin: SkinItem) => weapon_type ? skin.name.toLowerCase().includes(weapon_type.toLowerCase()) : true)
      .sort((a: SkinItem, b: SkinItem) => { return sort_by === "profit_high_to_low" ? b.profit - a.profit : 0 })
      .sort((a: SkinItem, b: SkinItem) => { return sort_by === "profit_low_to_high" ? a.profit - b.profit : 0 })
      .sort((a: SkinItem, b: SkinItem) => { return sort_by === "price_high_to_low" ? b.market_price - a.market_price : 0 })
      .sort((a: SkinItem, b: SkinItem) => { return sort_by === "price_low_to_high" ? a.market_price - b.market_price : 0 })
    : null


  return json({
    items: filtered_items,
    is_stattrak: is_stattrak !== null,
    weapon_type: weapon_type,
    sort_by: sort_by,
  });
}

export default function Index() {
  const submit = useSubmit();
  const { session } = useOutletContext<OutletContext>();
  const { items, is_stattrak, weapon_type, sort_by } = useLoaderData<typeof loader>();
  const formRef = useRef<HTMLFormElement>(null);

  console.log(session.user.id)
  const handleSubmit = ({ sort_by, weapon_type, is_stattrak } : { sort_by?: string, weapon_type?: string, is_stattrak?: boolean }) => {
    const formData = new FormData(formRef.current ?? undefined)

    console.log(is_stattrak)
    if (sort_by) {
      formData.set("sort_by", sort_by)
    }
    if (weapon_type) {
      formData.set("weapon_type", weapon_type)
    }
    if (is_stattrak == true) {
      formData.set("is_stattrak", "on")
    } else if (is_stattrak == false) {
      formData.delete("is_stattrak")
    }

    submit(formData, { replace: true });
  }

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
            <div className="flex items-center space-x-2">
              <Switch name="is_stattrak" checked={is_stattrak} onCheckedChange={(checked: boolean) => handleSubmit({ is_stattrak: checked })}/>
              <Label htmlFor="terms" className="min-w-[100px] base-small">Is StatTrak</Label>
            </div>
          </Form>
          <div className="gap-2 w-full justify-items-center inline-grid" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(210px, 1fr))", display: "grid" }}>
            {items?.map((item: SkinItem) => (
              <ItemCard item={item} key={item.link} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}