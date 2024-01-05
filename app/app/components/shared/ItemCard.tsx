import { Link } from "@remix-run/react";
import { SkinItem } from "~/types";

export default function ItemCard({ item }: { item: SkinItem }) {
  return (
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
          {/* <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', position: "absolute", top: "10px", left: '50%', transform: 'translateX(-50%)' }}>
            {item.stickers_icons.map((icon: string, stickerIndex: number) => (
              <img key={stickerIndex} src={icon} alt={`Sticker ${stickerIndex + 1}`} style={{ width: "auto", height: '30px', marginRight: '2px' }} />
          ))}
          </div> */}
          {/* <img src={item.image} alt={item.name} /> */}
          {/* <p>{item.name}</p>
          <p> {item.quality}</p>
          <p> {parseFloat(item.market_price).toFixed(2)}$</p> */}
          {/* <p> Steam Price: {parseFloat(item.steam_price).toFixed(2)}$</p>
          <p> Profit: {parseFloat(item.profit).toFixed(2)}%</p>
          <p> Stickers Price: {parseFloat(item.stickers_price).toFixed(2)}$</p> */}

          {/* <Link to={`/inventory`}>
             <img
               src={
                 post.creator?.imageUrl ||
                 "/assets/icons/profile-placeholder.svg"
               }
               alt="creator"
               className="w-12 lg:h-12 rounded-full"
             />
          </Link> */}

          <div className="flex flex-col w-full">
            <div className="flex gap-1">
              <p className="base-medium lg:body-bold text-light-1">
                ${parseFloat(item.market_price).toFixed(2)}
              </p>
              <p className="base-medium lg:body-bold text-secondary-500">+{parseInt(item.profit)}%</p>
            </div>
            <p className="base-medium lg:body-bold text-light-1">
              {item.quality}
            </p>
            <p className="mt-[2px] item-card_title text-grey">
              {item.name}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
