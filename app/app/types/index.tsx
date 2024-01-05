interface Sticker {
    id: string;
}

export interface SkinItem {
    name: string;
    type: string;
    is_stattrak: boolean;
    quality: string;
    market_price: number;
    steam_price: number;
    image: string;
    stickers_price: string;
    profit: number;
    link: string;
    stickers_instances: Sticker[];
    stickers_icons: string[];
}