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
import { createSupabaseServerClient } from "~/supabase.server";
import { Button } from "~/components/ui/button";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const response = new Response();

  const supabase = createSupabaseServerClient({ request, response });
  const url = new URL(request.url);
  const is_stattrak = url.searchParams.get("is_stattrak");
  const weapon_type = url.searchParams.get("weapon_type");
  const sort_by = url.searchParams.get("sort_by");
  const stickers_patern = url.searchParams.get("stickers_patern");
  const market_type = url.searchParams.get("market_type");
  const { data: items, error } = await supabase.rpc("get_all_skins");


  const filtered_items: SkinItem[] | null = items
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
      .map((skin: SkinItem) => ({
        ...skin,
        profit: (skin.stickers_price * 0.1 + skin.steam_price - skin.market_price) / skin.market_price * 100.0 
      }))
      .filter((skin: SkinItem) => is_stattrak === "on" ? skin.is_stattrak === true : true)
      .filter((skin: SkinItem) => weapon_type ? skin.name.toLowerCase().includes(weapon_type.toLowerCase()) : true)
      .filter((skin: SkinItem) => stickers_patern ? skin.stickers_patern === stickers_patern : true)
      .filter((skin: SkinItem) => market_type ? skin.market === market_type : true)
      .filter((skin: SkinItem) => skin.profit > 10)
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
    stickers_patern: stickers_patern,
    market_type: market_type
  });
}

export default function Index() {
  const submit = useSubmit();
  const { session } = useOutletContext<OutletContext>();
  const { items, is_stattrak, weapon_type, sort_by, stickers_patern, market_type } = useLoaderData<typeof loader>();
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
                  <SelectItem value="cs-money">cs.money</SelectItem>
                  <SelectItem value="skinbid">skinbid.com</SelectItem>
                  <SelectItem value="market-csgo">market.csgo.com</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <div className="flex items-center space-x-2">
              <Switch name="is_stattrak" checked={is_stattrak} onCheckedChange={(checked: boolean) => handleSubmit({ is_stattrak: checked })}/>
              <Label htmlFor="terms" className="min-w-[100px] base-small">Is StatTrak</Label>
            </div>
          </Form>
          <div className="gap-2 w-full justify-items-center inline-grid" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(170px, 1fr))", display: "grid" }}>
            {items?.map((item: SkinItem) => (
              <ItemCard item={item} key={item.link} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}