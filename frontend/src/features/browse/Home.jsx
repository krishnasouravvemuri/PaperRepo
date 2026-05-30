import Link from "next/link";

const FEATURES = [
  {
    title: "Question Papers",
    body: "Access past question papers for every subject. Practice with real exam questions and get familiar with the format.",
  },
  {
    title: "Important Questions",
    body: "Curated lists of important questions frequently asked in exams to help you study efficiently.",
  },
  {
    title: "Notes & PDFs",
    body: "Comprehensive notes, presentations, and PDFs for every topic. Study at your own pace.",
  },
];

export default function Home() {
  return (
    <>
      <section className="max-w-5xl mx-auto mt-16 p-8 bg-[#1c1b29] rounded-2xl shadow-2xl text-gray-100">
        <h1 className="text-4xl md:text-5xl font-extrabold text-teal-400 mb-6 text-center">
          Welcome to PaperRepo
        </h1>
        <p className="text-gray-300 text-lg mb-4 leading-relaxed text-center">
          Your ultimate destination for academic resources. From past question papers to important
          questions and comprehensive notes, everything you need in one place.
        </p>
        <p className="text-gray-300 text-lg mb-6 leading-relaxed text-center">
          Designed for students who want to study smarter, not harder.
        </p>
        <div className="flex justify-center">
          <Link
            href="/browse"
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 px-6 rounded-lg transition"
          >
            Browse Resources →
          </Link>
        </div>
      </section>

      <section className="max-w-5xl mx-auto mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        {FEATURES.map((f) => (
          <div key={f.title} className="bg-[#1c1b29] p-6 rounded-2xl shadow-lg text-center">
            <h2 className="text-teal-400 text-2xl font-bold mb-3">{f.title}</h2>
            <p className="text-gray-300 leading-relaxed">{f.body}</p>
          </div>
        ))}
      </section>

      <section className="max-w-5xl mx-auto mt-12 mb-8 text-center">
        <Link
          href="/login"
          className="inline-block bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-3 px-8 rounded-lg text-lg transition"
        >
          Upload and help others?
        </Link>
      </section>
    </>
  );
}
