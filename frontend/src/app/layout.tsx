import type { Metadata } from "next";
import {Toaster} from "react-hot-toast";
import { Inter } from "next/font/google";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Student Management | Ayush Agnihotri",
    description: "Created by Ayush Agnihotri",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="h-full bg-white dark">
            <body className={`${inter.className} h-full`}>
                <Toaster />
                {children}
            </body>
        </html>
    );
}
