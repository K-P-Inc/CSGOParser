import {
    Link,
    useLocation,
} from "@remix-run/react"
import React from "react";

const sidebarNavigation = [
    { name: 'Account', href: '/account' },
    { name: 'Inventory', href: '/inventory' },
    { name: 'Watchlist', href: '/watchlist' },
    { name: 'Settings', href: '/settings' },
];

export default function Layout({ children } : { children: React.ReactNode }) {
    const location = useLocation()

    const getDefaultColor = (href: string) => {
        console.log(location.pathname)
        return location.pathname === href ? "#0f7314" : "#4caf50"
    }

    return (
        <div style={{ display: "flex", height: "100vh" }}>
            <div
                style={{
                    minWidth: "min-content",
                    padding: "12px",
                    boxShadow: "10px 0 10px rgba(0, 0, 0, 0.3)",
                    flexDirection: "column",
                    display: "flex"
                }}
            >
                <ul className="space-y-4 font-medium">
                    {sidebarNavigation.map(item => 
                        <li key={item.name}>
                            <Link
                                style={{
                                    padding: "10px",
                                    marginBottom: "10px",
                                    backgroundColor: getDefaultColor(item.href),
                                    borderRadius: "4px",
                                    cursor: "pointer",
                                    listStyle: "none"
                                }}
                                className="flex items-center p-2"
                                onMouseEnter={(e: any) => { e.currentTarget.style.backgroundColor = "#0fd516" }}
                                onMouseLeave={(e: any) => { e.currentTarget.style.backgroundColor = getDefaultColor(item.href) }}
                                to={item.href}
                            >
                                {item.name}
                            </Link>
                    </li>
                    )}
                </ul>
            </div>
            <div style={{
                padding: '20px',
                width: '100%',
                boxSizing: 'border-box',
                overflow: 'auto',
                display: 'flex',
                flexWrap: 'wrap',
            }}>
                {children}
            </div>
        </div>
    );
}