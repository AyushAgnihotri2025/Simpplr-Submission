'use client'

import Cookies from "js-cookie";
import {useState, useEffect} from "react";
import {useRouter} from "next/navigation";

import API_HOST, {API_INITIAL} from "@/assets/creds";
import toast from "react-hot-toast";
import Popup from "@/components/popup";

export default function Home() {
    const [username, setUsername] = useState("admin");
    const [password, setPassword] = useState("test@1234");
    const router = useRouter();

    useEffect(() => {
        // Check if the token is available in the cookie
        const token = Cookies.get("Auth-Token");
        if (token) {
            // Redirect to dashboard if token is present
            router.push("/dashboard/search");
        }
    }, [router]);

    const handleLogin = async (event: { preventDefault: () => void; }) => {
        event.preventDefault();

        if (!username || !password) {
            return toast.error(
                "All fields are mandatory!",
                {
                    position: "top-right",
                    style: {
                        borderRadius: '10px',
                        background: '#333',
                        color: '#fff',
                    },
                }
            );
        }

        const toastId = toast.loading(
            "Verifying credentials!",
            {
                position: "top-right",
                style: {
                    borderRadius: '10px',
                    background: '#333',
                    color: '#fff',
                },
            }
        )

        try {
            const response = await fetch(new URL(`${API_INITIAL}/facultyLogin`, API_HOST), {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({username, password}),
            });

            const res = await response.json();

            if (!response.ok) {
                return toast.error(
                    res.message,
                    {
                        id: toastId,
                    }
                );
            }

            const token = res.token;

            // Save the token in a cookie with 1 hour expiration
            Cookies.set("Auth-Token", token, {expires: 1 / 24});

            toast.success(
                res.message,
                {
                    id: toastId,
                }
            );

            // Redirect to the dashboard
            await router.push("/dashboard/search");
        } catch (error) {
            console.error("Error during login:", error);
        }
    };

    return (
        <>
            <Popup/>
            <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8 dark:bg-gray-900">
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                    <img
                        className="mx-auto h-10 w-auto"
                        src="/favicon.png"
                        alt="Student Management"
                    />
                    <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900 dark:text-white">
                        Sign in to your account
                    </h2>
                </div>

                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                    <form className="space-y-6" onSubmit={handleLogin}>
                        <div>
                            <label
                                htmlFor="email"
                                className="block text-sm font-medium leading-6 text-gray-900 dark:text-white"
                            >
                                Email address/Username
                            </label>
                            <div className="mt-2">
                                <input
                                    id="email"
                                    name="email"
                                    type="text"
                                    autoComplete="email"
                                    required
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label
                                    htmlFor="password"
                                    className="block text-sm font-medium leading-6 text-gray-900 dark:text-white"
                                >
                                    Password
                                </label>
                                <div className="text-sm">
                                    <a
                                        href="#"
                                        className="font-semibold text-indigo-600 hover:text-indigo-500"
                                    >
                                        Forgot password?
                                    </a>
                                </div>
                            </div>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="current-password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                />
                            </div>
                        </div>

                        <div>
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                Sign in
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}
