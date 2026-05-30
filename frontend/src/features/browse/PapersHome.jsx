import Link from "next/link";

const CARDS = [
  { to: "/browse/question-papers", title: "Question Papers" },
  { to: "/browse/important-topics", title: "Important Topics" },
  { to: "/browse/materials", title: "Study Materials" },
];

export default function PapersHome() {
  return (
    <div className="mt-10">
      <h1 className="text-3xl font-bold text-teal-400 mb-8 text-center">Browse Resources</h1>
      <div className="flex justify-center">
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
