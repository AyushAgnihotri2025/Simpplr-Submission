import {AwaitedReactNode, JSXElementConstructor, Key, ReactElement, ReactNode, ReactPortal,
    useEffect,
    useState
} from "react";
import API_HOST, {API_INITIAL} from "@/assets/creds";
import Cookies from "js-cookie";
import {router} from "next/client";
import Link from "next/link";

export default function Table({auth_token}: {auth_token: string}) {
    const [data, setData] = useState([]);
    const [success, setSuccess] = useState(true);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(
                    new URL(`${API_INITIAL}/getAll?count=20`, API_HOST),
                    {
                        headers: {
                            "Authorization": `Bearer ${auth_token}`
                        }
                    }
                );
                const result = await response.json();
                if (result.success) {
                    setData(result.data || []);
                } else {
                    setError('Failed to fetch data');
                }
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Error fetching data');
            } finally {
                setLoading(false);
            }
        };

        if (auth_token) fetchData();
    }, [auth_token]);

    // @ts-ignore
    // @ts-ignore
    return (
        <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
            <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
                <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th scope="col" className="p-4">
                            <div className="flex items-center">
                                <input id="checkbox-all-search" type="checkbox"
                                       className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                                <label htmlFor="checkbox-all-search" className="sr-only">checkbox</label>
                            </div>
                        </th>
                        <th scope="col" className="px-6 py-3">
                            Student Id
                        </th>
                        <th scope="col" className="px-6 py-3 ">
                            <div className="flex items-center">
                                Student Name
                                <a href="#">
                                    <svg className="w-3 h-3 ms-1.5" aria-hidden="true"
                                         xmlns="http://www.w3.org/2000/svg"
                                         fill="currentColor" viewBox="0 0 24 24">
                                        <path
                                            d="M8.574 11.024h6.852a2.075 2.075 0 0 0 1.847-1.086 1.9 1.9 0 0 0-.11-1.986L13.736 2.9a2.122 2.122 0 0 0-3.472 0L6.837 7.952a1.9 1.9 0 0 0-.11 1.986 2.074 2.074 0 0 0 1.847 1.086Zm6.852 1.952H8.574a2.072 2.072 0 0 0-1.847 1.087 1.9 1.9 0 0 0 .11 1.985l3.426 5.05a2.123 2.123 0 0 0 3.472 0l3.427-5.05a1.9 1.9 0 0 0 .11-1.985 2.074 2.074 0 0 0-1.846-1.087Z"/>
                                    </svg>
                                </a>
                            </div>
                        </th>
                        <th scope="col" className="px-6 py-3">
                            D.O.B
                        </th>
                        <th scope="col" className="px-6 py-3">
                            Age
                        </th>
                        <th scope="col" className="px-6 py-3">
                            Class
                        </th>
                        <th scope="col" className="px-6 py-3">
                            Stream
                        </th>
                        <th scope="col" className="px-6 py-3">
                            Action
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr>
                                <td colSpan={13} className="px-6 py-4 text-center">Loading...</td>
                            </tr>
                        ) : (
                            (error != "") ? (
                                    <tr>
                                        <td colSpan={13} className="px-6 py-4 text-center">No Record Found...</td>
                                    </tr>
                                ) : (
                                    data.map((data: { student_id: Key | null | undefined; full_name: string | number | bigint | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<AwaitedReactNode> | null | undefined; date_of_birth: string | number | bigint | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<AwaitedReactNode> | null | undefined; age: string | number | bigint | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<AwaitedReactNode> | null | undefined; current_class: string | number | bigint | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<AwaitedReactNode> | null | undefined; stream: any; total_subjects: string | number | bigint | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<AwaitedReactNode> | null | undefined; total_marks: string | number | bigint | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<AwaitedReactNode> | null | undefined; percentage: number; grade: string; }) => (
                                    <tr
                                        key={data.student_id}
                                        className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                    >
                                        <td className="w-4 p-4">
                                            <div className="flex items-center">
                                                <input
                                                    id={`checkbox-table-search-${data.student_id}`}
                                                    type="checkbox"
                                                    className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                                                />
                                                <label htmlFor={`checkbox-table-search-${data.student_id}`} className="sr-only">checkbox</label>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">{data.student_id}</td>
                                        <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">{data.full_name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">{data.date_of_birth}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">{data.age}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">{data.current_class}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">{data.stream || 'N/A'}</td>
                                        <td className="flex items-center px-6 py-4">
                                            <Link href="#" className="font-medium text-blue-600 dark:text-yellow-500 hover:underline">View</Link>
                                            <Link href="#" className="font-medium text-blue-600 dark:text-blue-500 hover:underline ms-3">Edit</Link>
                                            <Link href="#" className="font-medium text-red-600 dark:text-red-500 hover:underline ms-3">Remove</Link>
                                        </td>
                                    </tr>
                                ))
                            )
                        )}
                    </tbody>
                </table>
            </div>
        </div>

    )
}