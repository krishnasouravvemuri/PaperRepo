"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/AuthContext.jsx";
import { useToast } from "../../context/ToastContext.jsx";

export default function Signup() {
  const { signup } = useAuth();
  const { notify } = useToast();
  const router = useRouter();
  const [form, setForm] = useState({ user_name: "", user_email: "", user_password: "" });
  const [busy, setBusy] = useState(false);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await signup(form);
      notify("Signup successful! Welcome.", "success");
      router.push("/upload");
    } catch (err) {
      notify(err.message || "Signup failed.", "error");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="flex justify-center mt-16">
      <form
        onSubmit={onSubmit}
        className="w-[28rem] max-w-full p-8 border border-gray-700 rounded-2xl bg-[#1e1e2e] shadow-2xl space-y-5"
      >
        <h1 className="text-3xl font-bold text-teal-400 text-center">Sign up</h1>
        <input
          name="user_name"
          placeholder="Username"
          value={form.user_name}
          onChange={onChange}
          required
          className="w-full p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <input
          name="user_email"
          type="email"
          placeholder="Email"
          value={form.user_email}
          onChange={onChange}
          required
          className="w-full p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <input
          name="user_password"
          type="password"
          placeholder="Password (min 8 chars)"
          value={form.user_password}
          onChange={onChange}
          required
          minLength={8}
          className="w-full p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <button
          type="submit"
          disabled={busy}
          className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-60 text-white font-semibold py-3 rounded-lg transition"
        >
          {busy ? "Creating…" : "Sign up"}
        </button>
        <p className="text-gray-400 text-center text-sm">
          Have an account?{" "}
          <Link href="/login" className="text-teal-400 hover:text-teal-300">
            Login
          </Link>
        </p>
      </form>
    </div>
  );
}
