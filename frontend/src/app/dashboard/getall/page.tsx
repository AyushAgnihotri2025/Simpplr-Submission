'use client'

import Image from "next/image";
import Header from "@/components/header";
import Popup from "@/components/popup";
import Table from "@/components/table";
import {useEffect, useState} from "react";
import Cookies from "js-cookie";
import {useRouter} from "next/navigation";

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
                    <Table auth_token={token}/>
                </div>
            </main>
        </main>
    );
}
