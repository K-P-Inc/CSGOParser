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