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
import { MarketCsgoIcon, CsmoneyIcon, SkinbidIcon, SkinportIcon, CsfloatIcon, DmarketIcon, BitskinsIcon, HaloSkinsIcon, SkinBaronIcon, WhiteMarketIcon, GamerPayIcon } from "~/assets/images";
import { Button } from "../ui/button";
import { useState } from "react";

function renderSection(title: string, rows : Array<{ label: string, value: number | string }>) {
  return (
    <div className="rounded border border-primary-500 bg-dark-2 p-3 space-y-2">
      <p className="small-regular text-grey">{title}</p>
      <div className="rounded border border-primary-500 px-4" />
      {rows.map((row, index) => (
        <div className="flex justify-between w-full" key={index}>
          <p className={"small-regular text-grey"}>
            {row.label}
          </p>
          <p className={"small-regular text-light-1"}>
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
  const [scrollTop, setScrollTop] = useState<number>(0);
  const openSteamLink = () => {
    const itemname = `${item.name} (${item.quality})`
    window.open(`https://steamcommunity.com/market/listings/730/${encodeURIComponent(itemname)}`, "_blank")
  }

  const openMarketLink = () => {
    let newWindow = window.open(item.market === "cs-money" ? item.link.split("&unique_id")[0] : item.link, "_blank");
  }

  const openInspectLink = () => {
    if (item.in_game_link) {
      window.open(item.in_game_link, "_blank")
    }
  }

  return (
    <AlertDialog>
      <AlertDialogContent className="space-y-4 max-w-[800px] p-0 pt-6">
        <div className="flex justify-between w-full px-6">
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
        <div
          onScroll={(event: any) => setScrollTop(event.target.scrollTop)}
          className={`space-y-4 custom-scrollbar max-h-[510px] ${scrollTop > 0 ? 'border-t' : ''} border-dark-4`}
          style={{ position: 'relative', overflowY: 'scroll' }}
        >
          <div className="flex justify-center w-full items-center space-x-4 p-6" style={{ position: 'relative' }}>
            <div className="flex items-center justify-center flex-col space-y-4" style={{ width: "67%" }}>
              <div className="item-card-popup_image flex items-center justify-center w-full">
                <img
                  style={{ zIndex: 2 }}
                  src={item.image}
                  alt="post image"
                  width={380}
                  loading="lazy"
                />
              </div>
              <div className="flex justify-center items-center w-full px-4 text-[12px] space-x-8 text-grey">
                <button onClick={openSteamLink}>
                  Open on Steam
                </button>
                {item.in_game_link &&
                  <button onClick={openInspectLink}>
                    Inspect in game
                  </button>
                }
              </div>
              <div className="rounded border border-dark-4 px-4 w-full"/>
              <div className="flex items-center justify-center w-full">
                {item.stickers_icons.map((icon: string, stickerIndex: number) => {
                    const stc_instance = item.stickers_instances.find((ins: Sticker) => icon.endsWith(ins.icon_url))
                    return (
                      <HoverCard openDelay={200} key={stickerIndex}>
                          <div className="w-[110px] items-center flex flex-col" style={{ position: 'relative' }}>
                            <p className="small-regular text-grey bg-dark-4 p-[3px] rounded-md" style={{ position: 'absolute', left: 0 }}>
                              {`${(((item.stickers_wears[stickerIndex] ?? 0)) * 100).toFixed(0)}%`}
                            </p>
                            <HoverCardTrigger>
                              <img
                                key={stickerIndex}
                                src={icon}
                                loading="lazy"
                                alt={`Sticker ${stickerIndex + 1}`}
                                className="h-[56px] hover:h-[62px] w-[65px] hover:w-[76px] object-cover hover:my-[-3px] mx-[5.5px] hover:mx-[0px] transition-all duration-100 ease-in"
                              />
                            </HoverCardTrigger>
                            <p className="small-regular text-center text-grey pt-1">
                                {`$${stc_instance?.price.toFixed(2)}`}
                            </p>
                          </div>
                        <HoverCardContent className="space-y-2 z-10" side={'top'}>
                          <p className="small-regular text-center text-light-1">
                            {stc_instance?.name}
                          </p>
                          <div className="flex justify-between w-full">
                            <p className="small-regular text-grey">
                              Price
                            </p>
                            <p className="small-regular text-light-1">
                              {`$${stc_instance?.price.toFixed(2)}`}
                            </p>
                          </div>
                          <div className="flex justify-between w-full">
                            <p className="small-regular text-grey">
                              Wear
                            </p>
                            <p className="small-regular text-light-1">
                              {`${(((item.stickers_wears[stickerIndex] ?? 0)) * 100).toFixed(0)}%`}
                            </p>
                          </div>
                        </HoverCardContent>
                      </HoverCard>
                    );
                })}
              </div>
            </div>
            <div className="space-y-4" style={{ width: "33%" }}>
              {renderSection("Prices", [
                renderRow("Steam", item.steam_price),
                renderRow("Market", item.market_price)
              ])}
              {renderSection("Stickers", [
                renderRow("Combo", item.stickers_patern),
                renderRow("Total", item.stickers_price),
              ])}
              {renderSection("Info", [
                renderRow("Pattern", item.pattern_template?.toString() ?? '-'),
                renderRow("Float", item.item_float?.toFixed(6) ?? '-'),
              ])}
              <div className="flex gap-1 body-bold text-[22px]">
                <p className="text-light-1">
                  ${parseFloat(item.market_price.toString()).toFixed(2)}
                </p>
                {item.market_price - (item.stickers_price * 0.1 + item.steam_price) < 0
                  ? <p className="text-green">-${((item.stickers_price * 0.1 + item.steam_price) - item.market_price).toFixed(2)}</p>
                  : <p className="text-secondary-500">+${(item.market_price - (item.stickers_price * 0.1 + item.steam_price)).toFixed(2)}</p>
                }
              </div>
                <Button
                  onClick={openMarketLink}
                  className="w-full rounded border border-primary-500 bg-dark-2 hover:border-green hover:bg-green transition"
                >
                  Buy item
                </Button>
            </div>
          </div>
        </div>
      </AlertDialogContent>
      <AlertDialogTrigger className="w-full">
      <div className="post-card space-y-2 p-3 h-full">
        <div className="flex w-full justify-center">
          {item.stickers_icons.map((icon: string, stickerIndex: number) => (
              <img key={stickerIndex} src={icon} alt={`Sticker ${stickerIndex + 1}`} width={33}/>
          ))}
        </div>
        <div className="flex items-center justify-center w-full" style={{ position: "relative" }}>
          <img
            style={{ zIndex: 2 }}
            src={item.image}
            alt="post image"
            className="post-card_img"
            loading="lazy"
          />
          <img
            style={{ zIndex: 1, position: 'absolute' }}
            loading="lazy"
            src={
              item.market === "skinbid" ? SkinbidIcon
                : item.market === "cs-money" ? CsmoneyIcon
                 : item.market === "market-csgo" ? MarketCsgoIcon
                  : item.market === "skinport" ? SkinportIcon
                    : item.market === "bitskins" ? BitskinsIcon
                      : item.market === "csfloat" ? CsfloatIcon
                        : item.market === "dmarket" ? DmarketIcon
                          : item.market === "haloskins" ? HaloSkinsIcon
                            : item.market === "skinbaron" ? SkinBaronIcon
                              : item.market === "white-market" ? WhiteMarketIcon
                                : item.market === "gamerpay" ? GamerPayIcon
                                  : ""
            }
            alt="post image"
            className="post-card_market_img"
          />
        </div>
        <div className="flex-between w-full">
          <div className="flex items-center gap-3 relative w-full">
            <div className="flex flex-col w-full space-y-3">
              <div className="flex flex-col w-full">
                <div className="flex gap-1 body-bold text-[22px]">
                  <p className="text-light-1">
                    ${parseFloat(item.market_price.toString()).toFixed(2)}
                  </p>
                  {parseInt(item.profit.toString()) !== 0 && (item.profit > 0
                    ? <p className="text-green">-{item.profit.toFixed(0)}%</p>
                    : <p className="text-secondary-500">+{(-1 * item.profit).toFixed(0)}%</p>
                  )}
                </div>
                <div className="flex gap-1 text-grey tiny-medium">
                  Suggested price: ${(item.stickers_price * 0.1 + item.steam_price).toFixed(2)}
                </div>
              </div>
              <div className="text-left text-light-1">
                <p className="tiny-medium">
                  {item.name.split('|')[0]}
                </p>
                <p className="text-[14px]">
                  {item.name.split('|')[1]}
                </p>
                <div className="flex space-x-1 text-sm text-grey">
                  <p className="text-grey">
                    {item.quality.split(item.quality.includes(" ") ? " " : "-").map(sl => sl[0]).join('')}
                  </p>
                  {item.item_float && (
                    <>
                      <p>/</p>
                      <p className="text-grey">
                        {item.item_float?.toFixed(6)}
                      </p>
                    </>
                  )}
                </div>
              </div>
              <Button
                onClick={(e: any) => {
                  e.stopPropagation(); 
                  openMarketLink()
                }}
                className="w-full rounded border border-dark-4 bg-dark-4 hover:border-primary-500 hover:bg-primary-500 transition h-[30px] text-[12px]"
              >
                {`Buy on ${item.market}`.toUpperCase().replace('-', '.')}
              </Button>
            </div>
          </div>
        </div>

      </div>
      </AlertDialogTrigger>
    </AlertDialog>
  )
}
