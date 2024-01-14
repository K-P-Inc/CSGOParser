import { cssBundleHref } from "@remix-run/css-bundle";
import type { LinksFunction } from "@remix-run/node";
import {
  Links,
  LiveReload,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";
import { useState } from "react";
import Layout from "./components/layout";
import stylesheet from "~/tailwind.css";
import { Navigate } from "react-router-dom";
import Auth from "./routes/auth";
import SigninForm from "./components/forms/SigninForm";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: stylesheet },
  ...(cssBundleHref ? [{ rel: "stylesheet", href: cssBundleHref }] : []),
];

export default function App() {
  const isAuthenticated = false;

  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {isAuthenticated ? (
          <>
            <Layout>
              <Outlet />
            </Layout>
            <ScrollRestoration />
            <Scripts />
            <LiveReload />
          </>
        ) : (
          <>
            <section className="flex flex-1 justify-center items-center flex-col py-10">
              <Auth />
            </section>
          </>
        )}
      </body>
    </html>
  );
};

//   return (
    // <html lang="en">
    //   <head>
    //     <meta charSet="utf-8" />
    //     <meta name="viewport" content="width=device-width, initial-scale=1" />
    //     <Meta />
    //     <Links />
    //   </head>
      // <body>
        // <Layout>
        //   <Outlet />
        // </Layout>
        // <ScrollRestoration />
        // <Scripts />
        // <LiveReload />
      // </body>
//     </html>
//   );
// }
