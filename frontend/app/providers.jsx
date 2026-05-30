"use client";

import Navbar from "../src/components/Navbar.jsx";
import Footer from "../src/components/Footer.jsx";
import { AuthProvider } from "../src/context/AuthContext.jsx";
import { ToastProvider } from "../src/context/ToastContext.jsx";

export default function Providers({ children }) {
  return (
    <ToastProvider>
      <AuthProvider>
        <div className="bg-gradient-to-br from-[#151320] to-[#100d18] text-gray-100 min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-grow pt-20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">{children}</div>
          </main>
          <Footer />
        </div>
      </AuthProvider>
    </ToastProvider>
  );
}
