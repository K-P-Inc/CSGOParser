import { useState } from "react";
import { Skeleton } from "../ui/skeleton"

export default function SkeletonItemCard() {
    const iconsUrl = [
        "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09G3h5SOhe7LPr7Vn35cppwpju2Z9N6l3AKx_0E6Mjv3IYOSIQc5MlGE-VW_kLu5jMLovs7LyyN9-n51sJxz0nI/512fx384f",
        "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uOxh7-Gw_alDK3UhH9Y78pOh-zF_Jn4xgW3_0FlNj_2dYbDdVU3MFqG_we-xe_tg8K8uZuYwXVh6XYh4X_dykGpwUYb-VH58g8/512fx384f",
        "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhjxszFJQJD_9W7m5a0mvLwOq7c2GpQ7JMg0uyYoYin2wHj-kU6YGD0cYOUcFA9YFnS_AC9xeq508K0us7XiSw0vgXM_Rw/512fx384f",
        "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJS_8W1nI-bluP8DLfYkWNFpsAh3bjE8Nqi2QLl_xdtYz3xcYCRc1I2MwzV_gK-yL-7jZfovZjNynR9-n5190ooeH8/512fx384f"
    ]
    const [iconUrl, _] = useState(iconsUrl[Math.floor(Math.random() * iconsUrl.length)]);

    return (
        <Skeleton className="w-full skeleton-post-card space-y-2 p-3 h-full">
            <div className="flex w-full justify-center space-x-[3px]">
            {[0, 1, 2, 3].map((i) => (
                <Skeleton key={i} className="bg-dark-4 w-[33px] h-[24.75px]"/>
            ))}
            </div>
            <Skeleton className="flex items-center justify-center w-full bg-dark-2" style={{ position: "relative" }}>
                <img
                    style={{ zIndex: 2 }}
                    src={iconUrl}
                    alt="post image"
                    className="skeleton-post-card_img bg-transition"
                />
            </Skeleton>
            <div className="flex-between w-full">
                <div className="flex items-center gap-3 relative w-full">
                    <div className="flex flex-col w-full space-y-3">
                        <div className="flex flex-col w-full space-y-1">
                            <div className="flex gap-1 body-bold text-[22px]">
                                <Skeleton className="bg-dark-4 h-[23.2px] w-[72px]" />
                                <Skeleton className="bg-dark-4 h-[23.2px] w-[48px]" />
                            </div>
                            <Skeleton className="bg-dark-4 h-[12px] w-[105px]" />
                        </div>
                        <div className="flex flex-col w-full space-y-1">
                            <Skeleton className="bg-dark-4 h-[12px] w-[72px]" />
                            <Skeleton className="bg-dark-4 h-[19px] w-[140px]" />
                            <Skeleton className="bg-dark-4 h-[18px] w-[105px]" />
                        </div>
                        <Skeleton className="bg-dark-4 h-[30px] w-full" />
                    </div>
                </div>
            </div>
        </Skeleton>
    )
}