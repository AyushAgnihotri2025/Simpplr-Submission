'use client'

import Header from "@/components/header";
import Popup from "@/components/popup";
import {useEffect, useState} from "react";
import Cookies from "js-cookie";
import {useRouter} from "next/navigation";

import SearchTable from "@/components/searchTable";

export default function DashBoard() {
    const router = useRouter();
    const [token, setToken] = useState("");

    useEffect(() => {
        // Check if the token is available in the cookie
        const token = Cookies.get("Auth-Token");
        if (!token) {
            // Redirect to dashboard if token is present
            router.push("/");
        } else {
            setToken(token);
        }
    }, [router]);

    return (
        <main className="dark:bg-gray-900 min-h-full">
            <Popup/>
            <Header/>
            <main className='dark:bg-gray-900'>
                <div className="mx-auto mt-2 max-w-7xl py-2 sm:px-6 lg:px-8 dark:bg-gray-900">
                    <SearchTable auth_token={token}/>
                </div>
            </main>
        </main>
    );
}
