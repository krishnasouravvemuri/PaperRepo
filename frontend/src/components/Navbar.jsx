"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../context/AuthContext.jsx";
import { useToast } from "../context/ToastContext.jsx";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { notify } = useToast();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    notify("Logged out successfully!", "success");
    router.push("/");
  };

  const links = user
    ? [
        { to: "/upload", label: "Home" },
        { to: "/my-uploads", label: "My Uploads" },
        { onClick: handleLogout, label: "Logout", danger: true },
      ]
    : [
        { to: "/login", label: "Upload" },
        { to: "/browse", label: "Browse Resources" },
      ];

  const renderLink = (l, mobile) => {
    const cls = `${l.danger ? "hover:text-red-400" : "hover:text-teal-300"} ${
      mobile ? "block text-right" : ""
    }`;
    if (l.onClick) {
      return (
        <button key={l.label} onClick={l.onClick} className={cls}>
          {l.label}
        </button>
      );
    }
    return (
      <Link key={l.label} href={l.to} className={cls} onClick={() => setOpen(false)}>
        {l.label}
      </Link>
    );
  };

  return (
    <nav className="fixed w-full top-0 z-30 bg-gradient-to-r from-[#221c35] to-[#1c1530] border-b border-teal-500/30 shadow-lg shadow-black/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link
            href={user ? "/upload" : "/"}
            className="text-2xl font-extrabold text-teal-400 hover:text-teal-300 transition"
          >
            PaperRepo
          </Link>

          <div className="hidden md:flex flex-1 justify-end items-center space-x-4">
            {links.map((l) => renderLink(l, false))}
          </div>

          <button
            onClick={() => setOpen((o) => !o)}
            className="md:hidden text-gray-300 hover:text-teal-400 focus:outline-none"
            aria-label="Toggle menu"
          >
            ☰
          </button>
        </div>
      </div>

      {open && (
        <div className="md:hidden flex flex-col space-y-2 p-4 bg-[#1c1b29] border-t border-[#2a2235] shadow-md">
          {links.map((l) => renderLink(l, true))}
        </div>
      )}
    </nav>
  );
}
