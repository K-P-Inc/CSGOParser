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
    { label: 'Database', route: '/database', icon: InventoryIcon },
    // { label: 'Watchlist', route: '/watchlist', icon: WatchlistIcon },
    // { label: 'Settings', route: '/settings', icon: SettingsIcon },
];

interface BarProperties {
    supabase?: SupabaseClient;
}

function TopBar({ supabase } : BarProperties) {

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

function LeftLayout({ supabase } : BarProperties) {
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
    </nav>
    )
}

interface LayoutProperties {
    children: React.ReactNode
}

export default function Layout({ children } : LayoutProperties) {
    return (
        <main className="flex h-screen">
            <div className="w-full md:flex h-full">
                <TopBar />
                <LeftLayout />
                <section className="flex flex-1 h-full">
                    {children}
                </section>
                <Bottombar />
            </div>
        </main>
    );
}