"use client";

import { createContext, useCallback, useContext, useState } from "react";

const ToastContext = createContext(null);

let nextId = 1;

const STYLES = {
  success: "bg-green-500",
  error: "bg-red-500",
  warning: "bg-orange-500",
  info: "bg-blue-500",
};

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const remove = useCallback((id) => {
    setToasts((t) => t.filter((x) => x.id !== id));
  }, []);

  const notify = useCallback(
    (message, type = "info") => {
      const id = nextId++;
      setToasts((t) => [...t, { id, message, type }]);
      setTimeout(() => remove(id), 3000);
    },
    [remove]
  );

  return (
    <ToastContext.Provider value={{ notify }}>
      {children}
      <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex flex-col gap-2">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`px-6 py-3 rounded-lg shadow-lg text-white font-semibold ${
              STYLES[t.type] || "bg-gray-800"
            }`}
          >
            {t.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);
