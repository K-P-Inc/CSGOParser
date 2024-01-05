import {
    Link,
    NavLink,
    useLocation,
} from "@remix-run/react"
import { AccountIcon, LogoIcon, InventoryIcon, WatchlistIcon, SettingsIcon } from "~/assets/images";
import React from "react";

const sidebarNavigation = [
    { label: 'Account', route: '/account', icon: AccountIcon },
    { label: 'Inventory', route: '/inventory', icon: InventoryIcon },
    { label: 'Watchlist', route: '/watchlist', icon: WatchlistIcon },
    { label: 'Settings', route: '/settings', icon: SettingsIcon },
];

function TopBar() {
    // const navigate = useNavigate();
    // const { user } = useUserContext();
    // const { mutate: signOut, isSuccess } = useSignOutAccount();

    // useEffect(() => {
    //     if (isSuccess) navigate(0);
    // }, [isSuccess]);

    return (
        <section className="topbar">
            <div className="flex-between py-4 px-5">
                <Link to="/" className="flex gap-3 items-center">
                <img
                    src={LogoIcon}
                    alt="logo"
                    width={130}
                    height={325}
                />
                </Link>
                <div className="flex gap-4">
                {/* <Button
                    variant="ghost"
                    className="shad-button_ghost"
                    onClick={() => signOut()}>
                    <img src="/assets/icons/logout.svg" alt="logout" />
                </Button>
                <Link to={`/profile/${user.id}`} className="flex-center gap-3">
                    <img
                    src={user.imageUrl || "/assets/icons/profile-placeholder.svg"}
                    alt="profile"
                    className="h-8 w-8 rounded-full"
                    />
                </Link> */}
                </div>
            </div>
        </section>
    );
}

function Bottombar () {
  const { pathname } = useLocation();

  return (
    <section className="bottom-bar">
      {sidebarNavigation.map((link) => {
        const isActive = pathname === link.route;
        return (
          <Link
            key={`bottombar-${link.label}`}
            to={link.route}
            className={`${
              isActive && "rounded-[10px] bg-primary-500 "
            } flex-center flex-col gap-1 p-2 transition`}>
            <img
                src={link.icon}
                alt={link.label}
                width={16}
                height={16}
                className={`${isActive && "invert-white"}`}
            />
            <p className="tiny-medium text-light-2">{link.label}</p>
          </Link>
        );
      })}
    </section>
  );
};


function LeftLayout() {
    const location = useLocation()

    return (
        <nav className="leftsidebar">
            <div className="flex flex-col gap-11">
                <Link to="/" className="flex gap-3 items-center">
                <img
                    src={LogoIcon}
                    alt="logo"
                    width={170}
                    height={36}
                />
                </Link>

                {/* {isLoading || !user.email ? (
                <div className="h-14">
                    <Loader />
                </div>
                ) : (
                <Link to={`/profile/${user.id}`} className="flex gap-3 items-center">
                    <img
                    src={user.imageUrl || "/assets/icons/profile-placeholder.svg"}
                    alt="profile"
                    className="h-14 w-14 rounded-full"
                    />
                    <div className="flex flex-col">
                    <p className="body-bold">{user.name}</p>
                    <p className="small-regular text-light-3">@{user.username}</p>
                    </div>
                </Link>
                )} */}

                <ul className="flex flex-col gap-6">
                    {sidebarNavigation.map((link: any) => {
                        const isActive = location.pathname === link.route;

                        return (
                            <li
                                key={link.label}
                                className={`leftsidebar-link group ${
                                    isActive && "bg-primary-500"
                                    }`}>
                                <NavLink
                                    to={link.route}
                                    className="flex gap-4 items-center p-4">
                                    <img
                                        src={link.icon}
                                        alt={link.label}
                                        width={32}
                                        height={32}
                                        className={`group-hover:invert-white ${
                                        isActive && "invert-white"
                                        }`}
                                    />
                                    {link.label}
                                </NavLink>
                            </li>
                        );
                    })}
                </ul>
            </div>

        {/* <Button
            variant="ghost"
            className="shad-button_ghost"
            onClick={(e) => handleSignOut(e)}>
            <img src="/assets/icons/logout.svg" alt="logout" />
            <p className="small-medium lg:base-medium">Logout</p>
        </Button> */}
    </nav>
    )
}
export default function Layout({ children } : { children: React.ReactNode }) {
    return (
        <main className="flex h-screen">
            <div className="w-full md:flex">
                <TopBar/>
                <LeftLayout/>
                <section className="flex flex-1 h-full">
                    {children}
                </section>
                <Bottombar />
            </div>
        </main>
    );
}