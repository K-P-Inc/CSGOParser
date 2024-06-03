import { cssBundleHref } from "@remix-run/css-bundle";
import type { LinksFunction } from "@remix-run/node";
import {
  Links,
  LiveReload,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useLoaderData,
  useRevalidator
} from "@remix-run/react";
import { createSupabaseServerClient } from "~/supabase.server";
import { createBrowserClient } from "@supabase/auth-helpers-remix";
import { LoaderFunctionArgs, json, redirect } from "@remix-run/node";
import { Toaster } from "./components/ui/toaster";
import Layout from "./components/layout";
import stylesheet from "~/tailwind.css";
import { IUserData } from "~/types"
import { useEffect, useState } from "react";
import { getSteamUserData } from "~/models/steam.api";
import { loadUser, updateUser } from "~/models/supabase.api";
import { getMarketCSGOBalance } from "~/models/market.csgo.api";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: stylesheet },
  ...(cssBundleHref ? [{ rel: "stylesheet", href: cssBundleHref }] : []),
];

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const env = {
    SUPABASE_URL: process.env.SUPABASE_URL!,
    SUPABASE_PUBLIC_KEY: process.env.SUPABASE_PUBLIC_KEY!,
  };

  const response = new Response();

  return json({ env }, { headers: response.headers });
};

export default function App() {
  const { env } = useLoaderData<typeof loader>();
  const [supabase] = useState(() => createBrowserClient(env.SUPABASE_URL, env.SUPABASE_PUBLIC_KEY));

  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <Layout supabase={supabase}>
          <Outlet context={{ supabase }} />
        </Layout>
        <Toaster />
        <ScrollRestoration />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
};
