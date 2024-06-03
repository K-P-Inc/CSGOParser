import { Link } from "@remix-run/react";
import { SkinItem, Sticker } from "~/types";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
  AlertDialogQuality
} from "../ui/alert-dialog";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "../ui/hover-card"
import { MarketCsgoIcon, CsmoneyIcon, SkinbidIcon } from "~/assets/images";
import { Button } from "../ui/button";

function renderSection(title: string, rows : Array<{ label: string, value: number | string }>) {
  return (
    <div className="rounded border border-primary-500 bg-dark-2 p-3 space-y-2">
      <p className="small-regular text-grey">{title}</p>
      <div className="rounded border border-primary-500 px-4" />
      {rows.map((row, index) => (
        <div className="flex justify-between w-full" key={index}>
          <p className={index === 0 ? "text-grey" : "small-regular text-grey"}>
            {row.label}
          </p>
          <p className={index === 0 ? "text-light-1" : "small-regular text-light-1"}>
            {typeof row.value === 'number' ? `$${row.value.toFixed(2)}` : row.value}
          </p>
        </div>
      ))}
    </div>
  );
}

function renderRow(label: string, value: number | string) {
  return { label, value };
}

export default function ItemCard({ item }: { item: SkinItem }) {
  const openSteamLink = () => {
    const itemname = `${item.name} (${item.quality})`
    window.open(`https://steamcommunity.com/market/listings/730/${encodeURIComponent(itemname)}`, "_blank")
  }
  const openMarketLink = () => {
    window.open(item.market === "cs-money" ? item.link.split("&unique_id")[0] : item.link, "_blank")
  }

  return (
    <AlertDialog>
      <AlertDialogContent className="space-y-4">
        <div className="flex justify-between w-full">
          <div className="space-y-1">
            <p className="item-card-popup_title text-left text-light-1">
              {item.name}
            </p>
            <p className="small-medium text-left text-grey">
              {item.quality}
            </p>
          </div>
          <AlertDialogCancel>X</AlertDialogCancel>
        </div>
        <div className="flex justify-center w-100 items-center space-x-4">
          <div className="flex items-center justify-center flex-col space-y-4" style={{ width: "60%" }}>
            <div className="item-card-popup_image flex items-center justify-center w-full">
              <img
                src={item.image}
                alt="post image"
                width={240}
              />
            </div>
            <div className="flex justify-center items-center w-full px-4 text-[12px] text-grey">
              <button onClick={openSteamLink}>
                Open on Steam
              </button>
            </div>
            <div className="rounded border border-dark-4 px-4 w-full"/>
            <div className="flex items-center justify-center w-full">
              {item.stickers_icons.map((icon: string, stickerIndex: number) => {
                  const stc_instance = item.stickers_instances.find((ins: Sticker) => icon.endsWith(ins.icon_url))
                  return (
                    <HoverCard openDelay={200} key={stickerIndex}>
                      <HoverCardTrigger>
                        <img
                          key={stickerIndex}
                          src={icon}
                          alt={`Sticker ${stickerIndex + 1}`}
                          className="h-[36px] hover:h-[42px] w-[45px] hover:w-[56px] object-cover hover:my-[-3px] mx-[5.5px] hover:mx-[0px] transition-all duration-100 ease-in"
                        />
                      </HoverCardTrigger>
                      <HoverCardContent className="space-y-2">
                        <p className="small-regular text-center text-light-1">
                          Sticker | {stc_instance?.name}
                        </p>
                        <div className="flex justify-between w-full">
                          <p className="small-regular text-grey">
                            Price
                          </p>
                          <p className="small-regular text-light-1">
                            {`$${stc_instance?.price.toFixed(2)}`}
                          </p>
                        </div>
                      </HoverCardContent>
                    </HoverCard>
                  );
              })}
            </div>
          </div>
          <div className="space-y-4" style={{ width: "40%" }}>
            {renderSection("Prices", [
              renderRow("Steam", item.steam_price),
              renderRow("Market", item.market_price)
            ])}
            {renderSection("Stickers", [
              renderRow("Pattern", item.stickers_patern),
              renderRow("Total", item.stickers_price),
            ])}
            <div className="flex gap-1">
              <p className="body-bold text-light-1">
                ${parseFloat(item.market_price.toString()).toFixed(2)}
              </p>
              <p className="body-bold text-secondary-500">+${(item.profit / 100.0 * item.market_price).toFixed(2)}</p>
            </div>
            {item.market === "cs-money" ? (
                <Button
                  onClick={openMarketLink}
                  className="w-full rounded border border-primary-500 bg-dark-2 hover:border-green hover:bg-green transition"
                >
                  Find item on market
                </Button>
              ) : (
                <Button
                  onClick={openMarketLink}
                  className="w-full rounded border border-primary-500 bg-dark-2 hover:border-green hover:bg-green transition"
                >
                  Buy item
                </Button>
              )
            }
          </div>
        </div>
      </AlertDialogContent>
      <AlertDialogTrigger className="w-full">
      <div className="post-card space-y-2">
        <div className="flex w-full justify-center">
          {item.stickers_icons.map((icon: string, stickerIndex: number) => (
              <img key={stickerIndex} src={icon} alt={`Sticker ${stickerIndex + 1}`} width={30}/>
          ))}
        </div>
        <div className="flex items-center justify-center w-full" style={{ position: "relative" }}>
          <img
            style={{ zIndex: 2 }}
            src={item.image}
            alt="post image"
            className="post-card_img"
          />
          <img
            style={{ zIndex: 1, position: 'absolute' }}
            src={
              item.market === "skinbid" ? SkinbidIcon 
                : item.market === "cs-money" ? CsmoneyIcon
                 : item.market === "market-csgo" ? MarketCsgoIcon
                  : ""
            }
            alt="post image"
            className="post-card_market_img"
          />
        </div>
        <div className="flex-between w-full px-5">
          <div className="flex items-center gap-3 relative w-full">
            <div className="flex flex-col w-full">
              <div className="flex gap-1">
                <p className="base-medium body-bold text-light-1">
                  ${parseFloat(item.market_price.toString()).toFixed(2)}
                </p>
                <p className="base-medium body-bold text-secondary-500">+{parseInt(item.profit.toString())}%</p>
              </div>
              <p className="text-left body-bold text-light-1" style={{ fontSize: "16px" }}>
                {item.quality}
              </p>
              <p className="mt-[2px] item-card_title text-grey">
                {item.name}
              </p>
            </div>
          </div>
        </div>
      </div>
      </AlertDialogTrigger>
    </AlertDialog>
  )
}
