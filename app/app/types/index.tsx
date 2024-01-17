export interface Sticker {
    id: string;
    price: number;
    icon_url: string;
    name: string;
}

export interface SkinItem {
    name: string;
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
}