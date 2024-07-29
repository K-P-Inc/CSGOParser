import { captureRemixErrorBoundaryError } from "@sentry/remix";
import { cssBundleHref } from "@remix-run/css-bundle";
import type { LinksFunction, MetaFunction } from "@remix-run/node";
import {
  Links,
  LiveReload,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useLoaderData,
  useRouteError,
  useLocation,
  Link,
} from "@remix-run/react";
import { createSupabaseServerClient } from "~/supabase.server";
import { createBrowserClient } from "@supabase/auth-helpers-remix";
import { LoaderFunctionArgs, json, redirect } from "@remix-run/node";
import { Toaster } from "./components/ui/toaster";
import Layout from "./components/layout";
import stylesheet from "~/tailwind.css";
import { IUserData } from "~/types";
import { useEffect, useState } from "react";
import { getSteamUserData } from "~/models/steam.api";
import { loadUser, updateUser } from "~/models/supabase.api";
import { getMarketCSGOBalance } from "~/models/market.csgo.api";
import { initGA, logPageView, initGTM, logGTMEvent } from './utils/analytics';
import { Button } from "~/components/ui/button";
import { FullLogoIcon } from "~/assets/images";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: stylesheet },
  {
    rel: 'icon',
    sizes: '192x192',
    type: 'image/png',
    href: '/android-chrome-192x192.png',
  },
  {
    rel: 'icon',
    sizes: '512x512',
    type: 'image/png',
    href: '/android-chrome-512x512.png',
  },
  {
    rel: 'apple-touch-icon',
    sizes: '180x180',
    href: '/apple-touch-icon.png',
  },
  {
    rel: 'icon',
    type: 'image/png',
    sizes: '32x32',
    href: '/favicon-32x32.png',
  },
  {
    rel: 'icon',
    type: 'image/png',
    sizes: '16x16',
    href: '/favicon-16x16.png',
  },
  {
    rel: 'icon',
    type: 'image/x-icon',
    href: '/favicon.ico',
  },
  ...(cssBundleHref ? [{ rel: "stylesheet", href: cssBundleHref }] : []),
];

export const meta: MetaFunction = () => {
  return [
    { title: "SKINHUB.PRO | Find the rarest CS2 items in the web" },
    {
      property: "og:title",
      content: "SKINHUB.PRO | Find the rarest CS2 items",
    },
    {
      property: "og:description",
      content: "Discover and buy rarest CS:GO and CS2 weapons with best floats, patterns and stickers combos at SKINHUB.PRO - your go-to marketplace for skins"
    },
    {
      property: "description",
      content: "Discover and buy rarest CS:GO and CS2 weapons with best floats, patterns and stickers combos at SKINHUB.PRO - your go-to marketplace for skins"
    },
    {
      property: "og:site_name",
      content: "SKINHUB.PRO",
    },
    {
      property: "og:type",
      content: "service",
    },
    {
      property: "og:image",
      content: "https://i.imgur.com/uYnMdd9.png"
    },
    {
      property: "og:image:height",
      content: "630"
    },
    {
      property: "og:image:width",
      content: "1200"
    },
    {
      name: "twitter:site",
      content: "@SkinhubPro"
    },
    {
      name: "twitter:creator",
      content: "@SkinhubPro"
    },
    {
      name: "twitter:card",
      content: "summary_large_image"
    },
    {
      name: 'og:date',
      content: '2024-05-16'
    },
    {
      name: 'og:coverage',
      content: 'world'
    },
    {
      name: 'og:source',
      content: 'https://skinhub.pro'
    },
    {
      name: 'og:provenance',
      content: 'https://skinhub.pro'
    },
    {
      name: 'og:rights_holder',
      content: 'https://skinhub.pro'
    },
    {
      name: "og:subject",
      content: "Explore and purchase the finest CS:GO and CS2 skins on SKINHUB.PRO, your premier analytics platform for skin trading with momental search of all skins on across multiple markets at the same time."
    },
    {
      name: "og:items_key_words",
      content: 'AWP, AK-47, M4A4, M4A1-S'
    },
    {
      name: 'og:markets_key_words',
      content: 'cs.money, bitskins, dmarket, steam, csfloat, haloskins, market, market.csgo, skinbid, skinport, white.market, skinbaron, gamerpay, waxpeer'
    },
    {
      name: 'og:search_key_words',
      content: 'CSGO, CS2, skins, skin, skinhub, weapon, knife, finishes, custom, virtual, trade, inventory, collection, gun, camouflage, pattern, design, rarity, value'
    }
  ];
};

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const env = {
    SUPABASE_URL: process.env.SUPABASE_URL!,
    SUPABASE_PUBLIC_KEY: process.env.SUPABASE_PUBLIC_KEY!,
  };

  const response = new Response();

  return json({ env }, { headers: response.headers });
};

export function ErrorBoundary() {
  const error = useRouteError();
  console.error(error);
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="mailru-domain" content="7s8VkUFnpzKSr4oy" />
        <Meta />
        <Links />
      </head>
      <body>
        <Layout>
        <div className="flex flex-col pt-16 pb-12"
              style={{ backgroundColor: "212429", flex: "0 0 100%", height: "100%", justifyContent: "center", display: "flex" }}
        >
        <div className="flex flex-col mt-16 mb-12" style={{ backgroundColor: "212429" }}>
            <main className="mx-auto flex w-full max-w-7xl flex-grow flex-col justify-center px-4 sm:px-6 lg:px-8">
              <div className="py-16">
                <div className="text-center">
                  <h2 className="text-9xl font-bold text-primary-500">404</h2>
                  <p className="text-xl text-white">
                    Sorry, we couldn’t find the page you’re looking for.
                  </p>
                  <div className="mt-6">
                  <Link to="/" className="text-xl font-medium text-primaryGreen">
                      Go back home
                      <span aria-hidden="true"> &rarr;</span>
                  </Link>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
        </Layout>
        <Toaster />
        <ScrollRestoration />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
}

export default function App() {
  const { env } = useLoaderData<typeof loader>();
  const location = useLocation();

  useEffect(() => {
    initGA();
  }, []);

  useEffect(() => {
    initGTM();
  }, []);

  useEffect(() => {
    logPageView(location.pathname + location.search);
  }, [location]);

  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="mailru-domain" content="7s8VkUFnpzKSr4oy" />
        <Meta />
        <Links />
      </head>
      <body>
        <Layout>
          <Outlet/>
        </Layout>
        <Toaster />
        <ScrollRestoration />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
}
