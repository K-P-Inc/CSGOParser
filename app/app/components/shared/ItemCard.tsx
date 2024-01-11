import { Link } from "@remix-run/react";
import { SkinItem } from "~/types";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "../ui/alert-dialog";

export default function ItemCard({ item }: { item: SkinItem }) {
  return (
    <AlertDialog>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{item.name} ({item.quality})</AlertDialogTitle>
            <AlertDialogDescription>
              <div className="flex w-full">
                {item.stickers_icons.map((icon: string, stickerIndex: number) => (
                    <img key={stickerIndex} src={icon} alt={`Sticker ${stickerIndex + 1}`} width={54} height={27}/>
                ))}
              </div>
              <div className="flex items-center justify-center w-full">
                <img
                  src={item.image}
                  alt="post image"
                  className=""
                />
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction>Buy</AlertDialogAction>
            <AlertDialogAction>Show in market</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
        <AlertDialogTrigger>
        <div className="post-card">
          <div className="flex w-full">
            {item.stickers_icons.map((icon: string, stickerIndex: number) => (
                <img key={stickerIndex} src={icon} alt={`Sticker ${stickerIndex + 1}`} width={32} height={18}/>
            ))}
          </div>
          <div className="flex items-center justify-center w-full">
            <img
              src={item.image}
              alt="post image"
              className="post-card_img"
            />
          </div>
          <div className="flex-between w-full">
            <div className="flex items-center gap-3 relative w-full">
              <div className="flex flex-col w-full">
                <div className="flex gap-1">
                  <p className="base-medium lg:body-bold text-light-1">
                    ${parseFloat(item.market_price.toString()).toFixed(2)}
                  </p>
                  <p className="base-medium lg:body-bold text-secondary-500">+{parseInt(item.profit.toString())}%</p>
                </div>
                <p className="base-medium text-left lg:body-bold text-light-1">
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
