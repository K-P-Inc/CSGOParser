import { defer, json, LinksFunction, type LoaderFunctionArgs } from "@remix-run/node";
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { createSupabaseServerClient } from "~/supabase.server";
import { FullLogoIcon, LogoIcon } from "~/assets/images";
import ItemCard from "~/components/shared/ItemCard";
import { Button } from "~/components/ui/button";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "~/components/ui/carousel"
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
// Import Swiper styles
import { SkinItem } from "~/types"
import { RDSClient } from "~/models/postgres.server";
import { Await, Link, useLoaderData } from "@remix-run/react";
import { Suspense, useEffect, useRef, useState } from "react";
import { loader as DBLoader } from "~/routes/database"
import SkeletonItemCard from "~/components/shared/SkeletonItemCard";
import Autoplay from "embla-carousel-autoplay"

const previewExamples = [
  {
    "name": "AK-47 | Bloodsport",
    "market": "csfloat",
    "type": "AK-47",
    "is_stattrak": false,
    "quality": "Minimal Wear",
    "market_price": 97.04,
    "steam_price": 119.32857142857144,
    "stickers_patern": "5-equal",
    "image": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhnwMzJemkV0966m4-PhOf7Ia_ummJW4NE_2LyV89Wt0QewqBE6Z2-lcY6UJlRrMF7SqQTvyO7shsK5v5idn3Rn6D5iuyjFoprsug/512fx384f",
    "profit": 21.703147872794126,
    "stickers_overprice": 3.34,
    "profit_based_on": "steam",
    "link": "https://csfloat.com/item/726821609914108725",
    "stickers_instances": [
        {
            "id": "75255ccf-efe6-4b2e-8a6a-7773e04e0997",
            "name": "Battle Scarred (Holo)",
            "price": 9.22,
            "icon_url": "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulRfXkPbQuqS0c7dVBJ2JBBDur-aOARhweHNdQJK49C5q4yKhfDxfbiGwzsCupdy3LrE84-ijA3n_kdrYjv7doWRJlc7Zl2Dq1e8wO7ug5Si_MOeoh93ilM",
        }
    ],
    "stickers_icons": [
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulRfXkPbQuqS0c7dVBJ2JBBDur-aOARhweHNdQJK49C5q4yKhfDxfbiGwzsCupdy3LrE84-ijA3n_kdrYjv7doWRJlc7Zl2Dq1e8wO7ug5Si_MOeoh93ilM",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulRfXkPbQuqS0c7dVBJ2JBBDur-aOARhweHNdQJK49C5q4yKhfDxfbiGwzsCupdy3LrE84-ijA3n_kdrYjv7doWRJlc7Zl2Dq1e8wO7ug5Si_MOeoh93ilM",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulRfXkPbQuqS0c7dVBJ2JBBDur-aOARhweHNdQJK49C5q4yKhfDxfbiGwzsCupdy3LrE84-ijA3n_kdrYjv7doWRJlc7Zl2Dq1e8wO7ug5Si_MOeoh93ilM",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulRfXkPbQuqS0c7dVBJ2JBBDur-aOARhweHNdQJK49C5q4yKhfDxfbiGwzsCupdy3LrE84-ijA3n_kdrYjv7doWRJlc7Zl2Dq1e8wO7ug5Si_MOeoh93ilM",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulRfXkPbQuqS0c7dVBJ2JBBDur-aOARhweHNdQJK49C5q4yKhfDxfbiGwzsCupdy3LrE84-ijA3n_kdrYjv7doWRJlc7Zl2Dq1e8wO7ug5Si_MOeoh93ilM"
    ],
    "stickers_price": 46.1,
    "stickers_wears": [
        null,
        null,
        null,
        null,
        null
    ],
    "order_type": "fixed",
    "item_float": 0.11209181696176529,
    "pattern_template": 564,
    "in_game_link": "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%2000180720FF042806300438E5A096EF0340B404620A080010D3241D00000000620A080110D3241D00000000620A080210D3241D00000000620A080310D3241D000000006214080010D3241D000000003D870D81BE4500BF24BBB67DA824"
  },
  {
    "name": "AWP | Redline",
    "market": "cs-money",
    "type": "AWP",
    "is_stattrak": false,
    "quality": "Field-Tested",
    "profit_based_on": "steam",
    "market_price": 54.74,
    "steam_price": 47.900000000000006,
    "stickers_overprice": 13.34,
    "stickers_patern": "4-equal",
    "image": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJB496klb-GkvP9Jrafxj0Iu5wh3r6V8I2i2QK3-0JlNW_0IYbAcQ5qN1-Dr1i-we27hJW_7oOJlyW4ZaUDog/512fx384f",
    "profit": 6.7143830947512,
    "link": "https://cs.money/market/buy/?search=AWP%20%7C%20Redline%20%28Field-Tested%29&sort=price&order=asc&minFloat=0.21978777&maxFloat=0.21978778&unique_id=22483576",
    "stickers_instances": [
        {
            "id": "00abb45e-9203-4a5a-8a40-2e12d847b228",
            "name": "Astralis (Holo) | Cologne 2016",
            "price": 26.95,
            "icon_url": "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DfQOqohZ-CBRJ1NhBFibKqJwgu0qORJWRHu97vx4aKzqGtMrmFxjkEvsN03b6W8I_w2AbtqRdtNzj2cpjVLFGevQIlLA",
        }
    ],
    "stickers_icons": [
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DfQOqohZ-CBRJ1NhBFibKqJwgu0qORJWRHu97vx4aKzqGtMrmFxjkEvsN03b6W8I_w2AbtqRdtNzj2cpjVLFGevQIlLA",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DfQOqohZ-CBRJ1NhBFibKqJwgu0qORJWRHu97vx4aKzqGtMrmFxjkEvsN03b6W8I_w2AbtqRdtNzj2cpjVLFGevQIlLA",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DfQOqohZ-CBRJ1NhBFibKqJwgu0qORJWRHu97vx4aKzqGtMrmFxjkEvsN03b6W8I_w2AbtqRdtNzj2cpjVLFGevQIlLA",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DfQOqohZ-CBRJ1NhBFibKqJwgu0qORJWRHu97vx4aKzqGtMrmFxjkEvsN03b6W8I_w2AbtqRdtNzj2cpjVLFGevQIlLA"
    ],
    "stickers_price": 107.8,
    "stickers_wears": [
        0,
        0,
        0,
        0
    ],
    "order_type": "fixed",
    "item_float": 0.21978777647018433,
    "pattern_template": 718,
    "in_game_link": "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561199423378949A38156409284D38885484631734339"
  },
  {
    name: "M4A1-S | Welcome to the Jungle",
    market: "skinport",
    type: "M4A1-S",
    is_stattrak: false,
    quality: "Battle-Scarred",
    market_price: 696.45426035328,
    steam_price: 978.54,
    image: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uO1gb-Gw_alDKjfl2BU1810i__Yu92i0Qbsr0A9ZG72I4SVJlI_MF2ErAK6kOvojZPpup_Oy3RrsyYj7XrD30vgGQS5Ta4/512fx384f',
    stickers_price: 224.04,
    stickers_patern: '4-equal',
    profit: 30.406351639052538,
    stickers_overprice: 40.34,
    link: "",
    stickers_instances:[
      {
        "id": "b5475d1e-65db-4c70-85e6-8643faa47e3a",
        "name": "Splyce (Foil) | MLG Columbus 2016",
        "price": 55.51,
        "icon_url": "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DFSua4xJ2DAgs7NhRbtYWjJA5snaHOIWVE6Nqwzdjala73ZuvSxT4Iuscl3uiRoI-t0AK1_RY9a2_1I9KLMlhpt_nMH1U",
      }
    ],
    stickers_icons: [
      "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DFSua4xJ2DAgs7NhRbtYWjJA5snaHOIWVE6Nqwzdjala73ZuvSxT4Iuscl3uiRoI-t0AK1_RY9a2_1I9KLMlhpt_nMH1U",
      "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DFSua4xJ2DAgs7NhRbtYWjJA5snaHOIWVE6Nqwzdjala73ZuvSxT4Iuscl3uiRoI-t0AK1_RY9a2_1I9KLMlhpt_nMH1U",
      "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DFSua4xJ2DAgs7NhRbtYWjJA5snaHOIWVE6Nqwzdjala73ZuvSxT4Iuscl3uiRoI-t0AK1_RY9a2_1I9KLMlhpt_nMH1U",
      "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXQ9QVcJY8gulReQ0DFSua4xJ2DAgs7NhRbtYWjJA5snaHOIWVE6Nqwzdjala73ZuvSxT4Iuscl3uiRoI-t0AK1_RY9a2_1I9KLMlhpt_nMH1U"
    ],
    stickers_wears: [0, 0, 0, 0],
    order_type: 'fixed',
    item_float: 0.1337322,
    pattern_template: null,
    profit_based_on: "steam",
    in_game_link: "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561199258580944A36459592498D4768995785271760750"
  }
]

export const links: LinksFunction = () => {
  const imageUrls = previewExamples.reduce((urls: any, example: any) => {
    urls.push(example.image);
    if (example.stickers_icons) {
      urls.push(...example.stickers_icons);
    }
    return urls;
  }, []).map((url: string) => ({
    rel: "preload",
    href: url,
    as: "image",
  }));

  return [...imageUrls, {
    rel: "stylesheet",
    href: "https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css",
  }]
};

export const loader = async (x: LoaderFunctionArgs) => {
  const url = new URL(x.request.url);
  // Add or modify query parameters
  url.searchParams.append('sort_by', 'profit_high_to_low');
  url.searchParams.append('stickers_patterns', '4-equal,5-equal');
  url.searchParams.append('sticker_types', 'Foil,Holo,Gold');
  url.searchParams.append('min_price', '20');
  url.searchParams.append('max_price', '200');

  const items = DBLoader(({ ...x, request: { ...x.request, url: url.toString() }})).then((response) => response.data.items);

  return defer({
    items: items,
    totalItems: 250321
  });
}


export default function Index() {
  const { items, totalItems } = useLoaderData<typeof loader>();
  const [liveSkins, setLiveSkins] = useState<SkinItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const autoplay = useRef(Autoplay({ delay: 2000 }));

  useEffect(() => {
    const updateSkins = async () => {
      const newSkins = await items;
      setLiveSkins(newSkins);
      setIsLoading(false);
    };

    updateSkins();
  }, [items]);

  return (
    <div className="base-element flex flex-1 flex-co">
      <div className="home-container text-center w-full">
        <div className="mx-auto flex flex-wrap items-center justify-center py-6 lg:py-12 w-full">
          <div className="text-center lg:text-left max-w-[550px]">
            <h1 className="text-4xl font-bold mb-4 text-white">
              A better way to find CS2 skins crafts offers
            </h1>
            <p className="text-sm mb-4 text-white">
              Skinhub.pro provides the most advanced tool and search engine for Counter Strike 2 skins crafts. Never waste your time again with handling multiple marketplaces or dealing with overpriced items — save your time and shop smarter!
            </p>
            <div className="space-x-4">
              <Link to="/database">
                <Button variant={"primary"} className="text-sm p-4">
                  BEST OFFERS
                </Button>
              </Link>
              <Button variant={"default"} className="text-sm p-4" onClick={() => window.open('https://x.com/SkinhubPro', '_blank')}>
                FOLLOW US
              </Button>
            </div>
          </div>
          <div className="mt-12 justify-center flex-container max-w-[600px]">
            {previewExamples.map((example, index) => (
              <div className="flex-item glassmorph transform3D max-w-[200px]" key={index}>
                <ItemCard onlyPreview={true} item={example as SkinItem}/>
              </div>
            ))}
          </div>
        </div>
        <div className="py-6 bg-dark-1 text-light-2 w-full">
          <div className="container mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6 text-white">ESSENTIAL NUMBERS</h2>
            <div className="flex flex-wrap justify-center h-full">
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4 h-full">
                <div className="px-6 py-10 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-primary-500">{(totalItems / 1000).toFixed(1)}K</h3>
                  <p>Avaliable items</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4 h-full">
                <div className="px-6 py-10 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-primary-500">2.3M</h3>
                  <p>Items found</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4 h-full">
                <div className="px-6 py-10 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-primary-500">99.9%</h3>
                  <p>Uptime guarantee</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4 h-full">
                <div className="px-6 py-10 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-primary-500">12</h3>
                  <p>Unique markets</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-center justify-center space-y-2 mt-12">
          <h2 className="text-3xl font-bold mb-6 text-white">LIVE ORDERS</h2>
          <Carousel
            plugins={[autoplay.current] as any}
            className="w-full max-w-[220px] sm:max-w-[440px] md:max-w-[440px] lg:max-w-[660px] xl:max-w-[900px] 2xl:max-w-[1140px] carousel-shadow border-primary-600 border-2 rounded-md p-2"
          >
            <CarouselContent className="-ml-1">
              {isLoading && [...Array(10).keys()].map(value => (
                <CarouselItem key={value} className="pl-1 basis-1/1 sm:basis-1/1 md:basis-1/2 lg:basis-1/3 xl:basis-1/4 2xl:basis-1/5">
                  <div className="p-1">
                    <SkeletonItemCard/>
                  </div>
                </CarouselItem>
              ))}
              {!isLoading && liveSkins.map((example, index) => (
                <CarouselItem key={index} className="pl-1 basis-1/1 sm:basis-1/1 md:basis-1/2 lg:basis-1/3 xl:basis-1/4 2xl:basis-1/5">
                  <div className="p-1">
                    <ItemCard item={example as SkinItem}/>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>

        {/* <div className="py-12 text-light-2 w-full">
          <div className="container mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6 text-primary-600">Features</h2>
            <div className="flex flex-wrap justify-center">
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-2 text-secondary-500">Feature 1</h3>
                  <p>Discover rare and valuable CS2 skins effortlessly.</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-2 text-secondary-500">Feature 2</h3>
                  <p>Access a comprehensive database of CS2 items.</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-2 text-secondary-500">Feature 3</h3>
                  <p>Get real-time updates on market trends.</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-2 text-secondary-500">Feature 4</h3>
                  <p>Personalized recommendations for your collection.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="py-12 bg-dark-1 text-light-2 w-full">
          <div className="container mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6 text-primary-600">Statistics</h2>
            <div className="flex flex-wrap justify-center">
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-green">500+</h3>
                  <p>Rare skins available</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-green">3000+</h3>
                  <p>Daily active users</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-green">99.9%</h3>
                  <p>Uptime guarantee</p>
                </div>
              </div>
              <div className="w-full sm:w-1/2 lg:w-1/4 p-4">
                <div className="p-6 bg-dark-2 rounded-lg">
                  <h3 className="text-2xl font-bold mb-2 text-green">24/7</h3>
                  <p>Customer support</p>
                </div>
              </div>
            </div>
          </div>
        </div> */}
      </div>
    </div>
  );
}
