import type { LoaderFunction } from "@remix-run/node";
import { redirect } from "@remix-run/node";

export const loader: LoaderFunction = async () => {
  const utmParameters = new URLSearchParams({
    utm_source: 'reddit',
    utm_campaign: 'post'
  });

  const targetUrl = `/?${utmParameters.toString()}`;

  return redirect(targetUrl);
};
