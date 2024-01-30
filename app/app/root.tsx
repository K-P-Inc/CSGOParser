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

  const supabase = createSupabaseServerClient({ request, response });

  const {
    data: { session },
  } = await supabase.auth.getSession();

  const requestURL = new URL(request.url)
  if (!session || !session.user) {
    if (!requestURL.pathname.startsWith("/auth")) {
      const searchParams = new URLSearchParams([["redirectTo", requestURL.pathname]]);
      throw redirect(`/auth?${searchParams}`,  {
        headers: response.headers
      });
    }
  } else if (requestURL.pathname.startsWith("/auth")) {
    throw redirect(requestURL.searchParams.get('redirectTo') ?? '/',  {
      headers: response.headers
    });
  }

  let data;
  if (session?.user.id) {
    data = await loadUser(supabase, session?.user.id);
    let updatedData = data

    if ((!data.icon_url || !data.steam_name) && data.steam_api_key && data.steam_id) {
      const steamdata = await getSteamUserData(data.steam_api_key, data.steam_id);

      updatedData = {
        ...updatedData,
        icon_url: steamdata.icon_url,
        steam_name: steamdata.steam_name
      }
    }

    if (!data.market_csgo_balance && data.market_csgo_api_key) {
      const marketbalance = await getMarketCSGOBalance(data.market_csgo_api_key)

      const currenyConverter = {
        "USD": marketbalance.money as number,
        "RUB": marketbalance.money / 90.0 as number,
        "EUR": marketbalance.money * 0.9 as number,
      }

      updatedData = {
        ...updatedData,
        market_csgo_balance: currenyConverter[marketbalance.currency as ("USD" | "RUB" | "EUR")],
      }
    }

    if (data !== updatedData) {
      data = await updateUser(supabase, session.user.id, updatedData)
    }
  }

  return json({ env, session, userDataLoaded: data }, { headers: response.headers });
};

export default function App() {
  const { env, session, userDataLoaded } = useLoaderData<typeof loader>();
  const { revalidate } = useRevalidator();
  const [userData, setUserData] = useState<IUserData>(userDataLoaded);
  const [supabase] = useState(() => createBrowserClient(env.SUPABASE_URL, env.SUPABASE_PUBLIC_KEY));

  const serverAccessToken = session?.access_token;

  useEffect(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      if (session?.access_token !== serverAccessToken) {
        revalidate();
      }
    });
    return () => {
      subscription.unsubscribe();
    };
  }, [supabase.auth, serverAccessToken, revalidate]);

  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {!session?.user ? (
          <Outlet context={{ supabase, session }} />
        ) : (
          <Layout supabase={supabase} userData={userData}>
            <Outlet context={{ userData, setUserData, supabase, session }} />
          </Layout>
        )}
        <Toaster />
        <ScrollRestoration />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
};
