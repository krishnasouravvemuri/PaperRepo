"use client";

import Link from "next/link";
import { useAuth } from "../../context/AuthContext.jsx";

const CARDS = [
  { to: "/upload/question-papers", title: "Question Papers" },
  { to: "/upload/important-topics", title: "Important Topics" },
  { to: "/upload/materials", title: "Study Materials" },
];

export default function UploadHome() {
  const { user } = useAuth();
  return (
    <div className="mt-10">
      <h1 className="text-3xl">Welcome {user?.user_name}</h1>
      <h2 className="text-xl mt-4">Contribute here:</h2>
      <div className="flex justify-center mt-8">
        <div className="w-[28rem] max-w-full p-8 border border-gray-700 rounded-2xl bg-[#1e1e2e] shadow-2xl">
          <ul className="space-y-6">
            {CARDS.map((c) => (
              <li key={c.to}>
                <Link
                  href={c.to}
                  className="text-xl bg-emerald-600 p-4 rounded-2xl hover:bg-emerald-500 block text-center transition"
                >
                  {c.title} →
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
