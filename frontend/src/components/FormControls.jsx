const inputCls =
  "w-full p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500";

export function FormCard({ title, onSubmit, children }) {
  return (
    <div className="flex justify-center mt-10 mb-8">
      <form
        onSubmit={onSubmit}
        className="w-[32rem] max-w-full p-8 border border-gray-700 rounded-2xl bg-[#1e1e2e] shadow-2xl space-y-5"
      >
        <h1 className="text-3xl font-bold text-teal-400 text-center">{title}</h1>
        {children}
      </form>
    </div>
  );
}

export function Input({ label, ...props }) {
  return (
    <div>
      {label && <label className="block mb-1 text-gray-300">{label}</label>}
      <input className={inputCls} {...props} />
    </div>
  );
}

export function Select({ label, options, ...props }) {
  return (
    <div>
      {label && <label className="block mb-1 text-gray-300">{label}</label>}
      <select className={inputCls} {...props}>
        <option value="">Select…</option>
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </div>
  );
}

export function FileInput({ label, ...props }) {
  return (
    <div>
      {label && <label className="block mb-1 text-gray-300">{label}</label>}
      <input
        type="file"
        className="w-full text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-emerald-600 file:text-white hover:file:bg-emerald-500"
        {...props}
      />
    </div>
  );
}

export function SubmitButton({ busy, children }) {
  return (
    <button
      type="submit"
      disabled={busy}
      className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-60 text-white font-semibold py-3 rounded-lg transition"
    >
      {busy ? "Saving…" : children}
    </button>
  );
}

export const EXAM_TYPES = ["CAT I", "CAT II", "FAT"];
export const SEMESTERS = ["FALL SEM", "WIN SEM", "Others"];
