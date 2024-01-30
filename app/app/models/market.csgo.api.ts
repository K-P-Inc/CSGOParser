export async function fetchMarketCSGOApi(path: string, api_key: string, query?: any ): Promise<any> {

    const response = await fetch(
        `https://market.csgo.com/api/v2/${path}?${new URLSearchParams({ ...query, key: api_key }).toString()}`, {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/json",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Upgrade-Insecure-Requests": "1",
                "Te": "trailers",
                "Connection": "close",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
                'Access-Control-Allow-Credentials': 'true'
            }
        }
    )

    if (!response.ok) {
        throw new Error(`Fetching https://market.csgo.com/api/v2/${path}?${new URLSearchParams({ ...query, key: api_key }).toString()} failed with ${response.status}`);
    }

    const body = await response.json();

    return body;
}


export async function getMarketCSGOBalance(api_key: string): Promise<any> {
    const response = await fetchMarketCSGOApi("get-money", api_key)

    return response;
}

export async function testMarketCSGOToken(api_key: string): Promise<boolean> {
    const response = await fetchMarketCSGOApi("test", api_key)

    return response.success === true;
}