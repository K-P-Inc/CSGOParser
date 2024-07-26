import { json, LoaderFunction } from "@remix-run/node";
import { SitemapStream, streamToPromise } from "sitemap";
import { Readable } from "stream";

const SITE_URL = "https://skinhub.pro";

export const loader: LoaderFunction = async () => {
  const links = [
    { url: '/', changefreq: 'weekly', priority: 1.0, lastmod: new Date().toISOString() },
    { url: '/database', changefreq: 'always', priority: 0.9, lastmod: new Date().toISOString() },
    // { url: '/watchlist', changefreq: 'weekly', priority: 0.5, lastmod: new Date().toISOString() },
    // { url: '/settings', changefreq: 'weekly', priority: 0.5, lastmod: new Date().toISOString() },
  ];

  const stream = new SitemapStream({ hostname: SITE_URL });
  const xmlData = await streamToPromise(Readable.from(links).pipe(stream)).then(data => data.toString());

  return new Response(xmlData, {
    headers: {
      "Content-Type": "application/xml"
    }
  });
};
