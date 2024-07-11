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
      content: "SKINHUB.PRO | Find the rarest CS2 items in the web",
    },
    {
      property: "og:description",
      content: "Best platform to find rarest and most profitable CS2 stickers combos on the markets",
    },
    {
      property: "og:image",
      content: "https://i.imgur.com/f3O055M.png"
    },
    {
      property: "og:image:width",
      content: "4096"
    },
    {
      property: "og:image:height",
      content: "1714"
    },
    {
      property: "og:image:type",
      content: "image/png"
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

export const ErrorBoundary = () => {
  const error = useRouteError();
  captureRemixErrorBoundaryError(error);
  return <div>Something went wrong</div>;
};

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
