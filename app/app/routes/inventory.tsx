import { useLoaderData } from "@remix-run/react";
import { RDSClient } from "~/models/postgres.server";
import PriceFilter from './filter';

export async function loader() {
  const postgresClient = new RDSClient();
  let items = await postgresClient.query(
    `
        SELECT
        weapons_prices.name,
        weapons_prices.is_stattrak,
        weapons_prices.quality,
        skins.price AS market_price,
        weapons_prices.price AS steam_price,
        weapons_prices.icon_url,
        skins.stickers_price,
        skins.profit,
        skins.link
        FROM skins
        INNER JOIN weapons_prices ON skins.skin_id = weapons_prices.id
    `
  );

  return items
    ? items.map((row) => ({
        name: `${row["is_stattrak"] ? "StatTrak™ " : ""}${row["name"]}`,
        quality: `${row["quality"]}`,
        market_price: `${row["market_price"]}$`,
        steam_price: `${row["steam_price"]}$`,
        image: `https://community.akamai.steamstatic.com/economy/image/${row["icon_url"]}`,
        stickers_price: `${row["stickers_price"]}`,
        profit: `${row["profit"]}`,
        link: `${row["link"]}`,
      }))
    : null;
}

export default function Index() {
  const data = useLoaderData<typeof loader>();

  const inventoryItemStyle = {
    width: "200px", // Increase the maximum width
    height: "420px",
    backgroundColor: "#363636",
    color: "#fff",
    padding: "10px",
    margin: "10px",
    borderRadius: "4px",
    textAlign: "center" as const,
    // flex: "0 1 calc(25% - 20px)",
    boxSizing: "border-box" as const,
    border: "1px solid #4caf50",
    marginRight: "10px",
    marginLeft: "10px",
  };

  const imgStyle = {
    maxWidth: "100%",
    height: "auto",
    borderRadius: "4px",
    marginBottom: "5px",
  };

  const pStyle = {
    marginBlockStart: "1em",
    marginBlockEnd: "1em",
    marginInlineStart: "0px",
    marginInlineEnd: "0px",
    fontSize: "14px",
    lineHeight: "16px"
  };

  const buttonStyle = {
    padding: "5px 10px",
    backgroundColor: "#4caf50",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  };

  const openLink = (link: string) => {
    window.open(link, "_blank");
  };

  return (
    <>
      {data?.map((item: any, index: number) => (
        <div key={index} style={inventoryItemStyle}>
          <img style={imgStyle} src={item.image} alt={item.name} />
          <p style={{ ...pStyle, height: "48px" }}>{item.name}</p>
          <p style={pStyle}>{item.quality}</p>
          <p style={pStyle}>{parseFloat(item.market_price).toFixed(2)}$</p>
          <p style={pStyle}>Steam Price: {parseFloat(item.steam_price).toFixed(2)}$</p>
          <p style={pStyle}>Profit: {parseFloat(item.profit).toFixed(2)}%</p>
          <p style={pStyle}>Stickers Price: {parseFloat(item.stickers_price).toFixed(2)}$</p>
          <button
            style={buttonStyle}
            onClick={() => openLink(item.link)}
          >
            Inspect
          </button>
        </div>
      ))}
    </>
  );
}