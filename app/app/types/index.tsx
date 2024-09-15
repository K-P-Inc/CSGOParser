import React from 'react';
import type { Session, SupabaseClient } from "@supabase/supabase-js";

export interface Sticker {
    id: string;
    price: number;
    icon_url: string;
    name: string;
}

export interface SkinItem {
    id: string;
    name: string;
    market: string;
    type: string;
    is_stattrak: boolean;
    quality: string;
    market_price: number;
    steam_price: number;
    image: string;
    stickers_price: number;
    stickers_patern: string;
    profit: number;
    link: string;
    stickers_instances: Sticker[];
    stickers_icons: string[];
    stickers_wears: number[] | null[];
    stickers_overprice: number;
    profit_based_on: "steam" | "buff";
    order_type: string;
    item_float: number | null;
    pattern_template: number | null;
    in_game_link: string | null
}

export type INavLink = {
    imgURL: string;
    route: string;
    label: string;
  };

export type IUpdateUser = {
  userId: string;
  name: string;
  bio: string;
  imageId: string;
  imageUrl: URL | string;
  file: File[];
};

export type INewPost = {
  userId: string;
  caption: string;
  file: File[];
  location?: string;
  tags?: string;
};

export type IUpdatePost = {
  postId: string;
  caption: string;
  imageId: string;
  imageUrl: URL;
  file: File[];
  location?: string;
  tags?: string;
};

export type IUser = {
  id: string;
  name: string;
  username: string;
  email: string;
  imageUrl: string;
  bio: string;
};

export type INewUser = {
  name: string;
  email: string;
  username: string;
  password: string;
};

export interface IUserData {
  id: string;
  steam_id: string;
  steam_api_key: string;
  steam_name: string;
  icon_url: string;
  market_csgo_api_key: string;
  market_csgo_balance: number;
}

export type OutletContext = {
  userData: IUserData;
  setUserData: React.Dispatch<React.SetStateAction<IUserData>>;
  supabase: SupabaseClient;
  session: Session;
};

export type WearType = "Factory New" | "Minimal Wear" | "Field-Tested" | "Well-Worn" | "Battle-Scarred";
export type WeaponType = "AK-47" | "M4A4" | "M4A1-S" | "AWP" |  "SSG 08" | "SG 553" | "AUG" | "FAMAS" |  "Galil AR" | "USP-S" | "Glock-18" | "Desert Eagle" | "P250";
export type ShopType = "bitskins.com" | "cs.money" | "csfloat.com" | "dmarket.com" | "haloskins.com" | "market.csgo.com" | "skinbid.com" | "skinport.com" | "white.market" | "skinbaron.de" | "gamerpay.gg" | "waxpeer.com";
export type StickersPattern = "5-equal" | "4-equal" | "3-equal" | "2-equal" | "other";
export type StickersType = "Gold" | "Foil" | "Holo" | "Glitter";
export type SortType = "newest" | "oldest" | "profit_high_to_low" | "profit_low_to_high" | "price_high_to_low" | "price_low_to_high";
export type CategoryType = "StatTrak™" | "Normal"
