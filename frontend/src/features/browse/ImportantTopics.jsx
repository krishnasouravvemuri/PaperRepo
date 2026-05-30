"use client";

import { useEffect, useState } from "react";
import { listImportantTopics, getImportantTopicFileUrl } from "../../api/importantTopics.js";
import { useToast } from "../../context/ToastContext.jsx";

const EXAM_TYPES = ["CAT I", "CAT II", "FAT"];

export default function ImportantTopics() {
  const { notify } = useToast();
  const [filters, setFilters] = useState({ course_code: "", exam_type: "" });
  const [topics, setTopics] = useState([]);
  const [searched, setSearched] = useState(false);

  const load = async (params) => {
    try {
      setTopics((await listImportantTopics(params)) || []);
    } catch (err) {
      notify(err.message || "Failed to load.", "error");
    }
  };

  useEffect(() => {
    load({});
  }, []);

  const onSearch = (e) => {
    e.preventDefault();
    setSearched(true);
    load(filters);
  };

  const openFile = async (id, download) => {
    try {
      const { url } = await getImportantTopicFileUrl(id);
      if (download) {
        const a = document.createElement("a");
        a.href = url;
        a.download = "";
        a.click();
      } else {
        window.open(url, "_blank", "noopener");
      }
    } catch (err) {
      notify(err.message || "Could not open file.", "error");
    }
  };

  return (
    <div className="flex flex-col gap-6 mt-10">
      <form onSubmit={onSearch} className="flex flex-col space-y-4">
        <label className="text-2xl font-semibold text-gray-200">Search for Important Topics:</label>
        <div className="flex flex-wrap gap-4">
          <input
            placeholder="Course Code"
            value={filters.course_code}
            onChange={(e) => setFilters({ ...filters, course_code: e.target.value })}
            className="p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] max-w-md text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <select
            value={filters.exam_type}
            onChange={(e) => setFilters({ ...filters, exam_type: e.target.value })}
            className="p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">Exam Type</option>
            {EXAM_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className="font-semibold bg-emerald-600 px-4 py-2 rounded-xl hover:bg-emerald-500 transition"
          >
            Search
          </button>
        </div>
      </form>
      <p className="font-semibold text-gray-300">Enter the course code in capitals for best results.</p>

      {topics.length > 0 ? (
        <div className="mt-4 p-6 bg-[#1e1e2e] rounded-2xl shadow-2xl overflow-x-auto mb-4">
          <h2 className="text-2xl font-semibold mb-4">Results:</h2>
          <table className="min-w-full text-left border border-gray-700 rounded-lg">
            <thead className="bg-[#221c35] text-teal-400">
              <tr>
                {["Sl No", "Title", "Subject", "Code", "Exam", "Faculty", "Actions"].map((h) => (
                  <th key={h} className="px-4 py-2 border-r border-gray-600">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {topics.map((t, i) => (
                <tr key={t.important_topic_id} className="border-b border-gray-700 hover:bg-[#2a2235]">
                  <td className="px-4 py-2 border-r border-gray-600">{i + 1}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{t.important_topic_title}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{t.subject_name}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{t.subject_code}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{t.important_topic_exam_type}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{t.faculty_name || "-"}</td>
                  <td className="px-4 py-2 flex gap-2 justify-center">
                    <button
                      onClick={() => openFile(t.important_topic_id, false)}
                      className="px-2 py-1 bg-blue-500 rounded text-white hover:bg-blue-400"
                    >
                      View
                    </button>
                    <button
                      onClick={() => openFile(t.important_topic_id, true)}
                      className="px-2 py-1 bg-green-500 rounded text-white hover:bg-green-400"
                    >
                      Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        searched && <p className="mt-6 text-gray-400">No topics found.</p>
      )}
    </div>
  );
}
