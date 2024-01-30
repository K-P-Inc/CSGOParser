import {
    Link,
    NavLink,
    useLocation,
} from "@remix-run/react"
import { AccountIcon, LogoIcon, InventoryIcon, WatchlistIcon, SettingsIcon, LogoutIcon } from "~/assets/images";
import React from "react";
import { SupabaseClient } from "@supabase/auth-helpers-remix";
import { Button } from "./ui/button";

const sidebarNavigation = [
    { label: 'Account', route: '/account', icon: AccountIcon },
    { label: 'Inventory', route: '/inventory', icon: InventoryIcon },
    // { label: 'Watchlist', route: '/watchlist', icon: WatchlistIcon },
    // { label: 'Settings', route: '/settings', icon: SettingsIcon },
];

interface BarProperties {
    supabase: SupabaseClient;
    userData: any;
}

function TopBar({ supabase, userData } : BarProperties) {

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
                <Button
                    variant="ghost"
                    className="shad-button_ghost"
                    onClick={() => { supabase.auth.signOut() }}>
                   <img src={LogoutIcon} width={32} height={32} alt="logout"/>
                </Button>
                <div className="flex-center gap-3">
                    <img
                        src={userData?.icon_url || AccountIcon}
                        alt="profile"
                        className="h-8 w-8 rounded-full"
                    />
                </div>
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

function LeftLayout({ supabase, userData } : BarProperties) {
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

                <div className="flex gap-3 items-center">
                    <img
                        src={userData?.icon_url || AccountIcon}
                        alt="profile"
                        className="h-14 w-14 rounded-full"
                    />
                    <div className="flex flex-col">
                    <p className="body-bold">{userData?.steam_name || "Steam name"}</p>
                    <p className="small-regular text-light-3">${userData && userData.market_csgo_balance ? userData?.market_csgo_balance.toFixed(2) : '$$$'}</p>
                    </div>
                </div>

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

        <Button
            variant="ghost"
            className="shad-button_ghost"
            onClick={() => { supabase.auth.signOut() }}>
            <img className="text-primary-500 stroke-primary-500" src={LogoutIcon} width={32} height={32} alt="logout"/>
            <p className="small-medium lg:base-medium">Logout</p>
        </Button>
    </nav>
    )
}

interface LayoutProperties {
    supabase: SupabaseClient;
    userData: any;
    children: React.ReactNode
}

export default function Layout({ supabase, userData, children } : LayoutProperties) {
    return (
        <main className="flex h-screen">
            <div className="w-full md:flex">
                <TopBar supabase={supabase} userData={userData}/>
                <LeftLayout supabase={supabase} userData={userData}/>
                <section className="flex flex-1 h-full">
                    {children}
                </section>
                <Bottombar />
            </div>
        </main>
    );
}