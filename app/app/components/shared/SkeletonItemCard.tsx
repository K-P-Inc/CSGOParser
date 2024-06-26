import { useState } from "react";
import { Skeleton } from "../ui/skeleton"

export default function SkeletonItemCard() {
    const iconsUrl = [
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhjxszFJTwW0924l4WYg-X1P4Tdn2xZ_ItyiO2Yot-n3gztrUduMW6icdWcc1RqM1HR_FfswLu6gZe4tZrNmiBkpGB8smM7Zio1",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV092lnYmGmOHLP7LWnn8fvpMkjOqS99Smiwzk_0VvamH0LIHEdwFqYw2G_QC3lefsjZS4uJXLyWwj5HclxVTx0A",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJS_8W1nI-bluP8DLfYkWNFppQgj7yV9Nqi2Fbj_Eo5Ym72I9XGJwc2NAnS_1Pqxu6615W575uYznd9-n51iddPieY",
        "https://community.akamai.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uO3mb-Gw_alfqjul2dd59xOhfvA-4vwt1mxrxopPnfxIoPAcgQ6NQqGq1O6kO_vjZa46JWdwHAw6XNwsSvVmxzh0B4abLFnm7XAHsAw1GuT"
    ]
    const [iconUrl, _] = useState(iconsUrl[Math.floor(Math.random() * iconsUrl.length)]);

    return (
        <Skeleton className="w-full skeleton-post-card space-y-2">
            <div className="flex w-full justify-center space-x-[3px]">
            {[0, 1, 2, 3].map((i) => (
                <Skeleton key={i} className="bg-dark-4 w-[27px] h-[22.5px]"/>
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
            <div className="flex-between w-full px-5">
                <div className="flex items-center gap-3 relative w-full">
                    <div className="flex flex-col w-full">
                        <div className="flex gap-[5px]">
                            <Skeleton className="bg-dark-4 h-[24px] w-[72px]" />
                            <Skeleton className="bg-dark-4 h-[24px] w-[48px]" />
                        </div>
                        <Skeleton className="bg-dark-4 mt-[5px] h-[19px] w-[105px]" />
                        <Skeleton className="bg-dark-4 mt-[5px] h-[25px] w-[145px]"/>
                    </div>
                </div>
            </div>
        </Skeleton>
    )
}