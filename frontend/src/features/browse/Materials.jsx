"use client";

import { useEffect, useState } from "react";
import { listMaterials, getMaterialFileUrl } from "../../api/materials.js";
import { downloadFromUrl } from "../../api/download.js";
import Spinner from "../../components/Spinner.jsx";
import { useToast } from "../../context/ToastContext.jsx";

export default function Materials() {
  const { notify } = useToast();
  const [filters, setFilters] = useState({ course_code: "", topic_type: "" });
  const [materials, setMaterials] = useState([]);
  const [searched, setSearched] = useState(false);
  const [downloadingId, setDownloadingId] = useState(null);

  const load = async (params) => {
    try {
      setMaterials((await listMaterials(params)) || []);
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
    if (download && downloadingId) return;
    try {
      if (download) {
        setDownloadingId(id);
        const { url, filename } = await getMaterialFileUrl(id);
        await downloadFromUrl(url, filename);
      } else {
        const { url } = await getMaterialFileUrl(id);
        window.open(url, "_blank", "noopener");
      }
    } catch (err) {
      notify(err.message || "Could not open file.", "error");
    } finally {
      if (download) setDownloadingId(null);
    }
  };

  return (
    <div className="flex flex-col gap-6 mt-10">
      <form onSubmit={onSearch} className="flex flex-col space-y-4">
        <label className="text-2xl font-semibold text-gray-200">Search for Study Materials:</label>
        <div className="flex flex-wrap gap-4">
          <input
            placeholder="Course Code"
            value={filters.course_code}
            onChange={(e) => setFilters({ ...filters, course_code: e.target.value })}
            className="p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] max-w-md text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <input
            placeholder="Topic Type"
            value={filters.topic_type}
            onChange={(e) => setFilters({ ...filters, topic_type: e.target.value })}
            className="p-3 rounded-lg border border-gray-600 bg-[#2a2a3d] max-w-md text-gray-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <button
            type="submit"
            className="font-semibold bg-emerald-600 px-4 py-2 rounded-xl hover:bg-emerald-500 transition"
          >
            Search
          </button>
        </div>
      </form>
      <p className="font-semibold text-gray-300">Enter the course code in capitals for best results.</p>

      {materials.length > 0 ? (
        <div className="mt-4 p-6 bg-[#1e1e2e] rounded-2xl shadow-2xl overflow-x-auto mb-4">
          <h2 className="text-2xl font-semibold mb-4">Results:</h2>
          <table className="min-w-full text-left border border-gray-700 rounded-lg">
            <thead className="bg-[#221c35] text-teal-400">
              <tr>
                {["Sl No", "Title", "Subject", "Code", "Topic Type", "Faculty", "Actions"].map((h) => (
                  <th key={h} className="px-4 py-2 border-r border-gray-600">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {materials.map((m, i) => (
                <tr key={m.material_id} className="border-b border-gray-700 hover:bg-[#2a2235]">
                  <td className="px-4 py-2 border-r border-gray-600">{i + 1}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{m.material_title}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{m.subject_name}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{m.subject_code}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{m.material_topic_type}</td>
                  <td className="px-4 py-2 border-r border-gray-600">{m.faculty_name || "-"}</td>
                  <td className="px-4 py-2 flex gap-2 justify-center">
                    <button
                      onClick={() => openFile(m.material_id, false)}
                      className="px-2 py-1 bg-blue-500 rounded text-white hover:bg-blue-400"
                    >
                      View
                    </button>
                    <button
                      onClick={() => openFile(m.material_id, true)}
                      disabled={downloadingId === m.material_id}
                      className="px-2 py-1 bg-green-500 rounded text-white hover:bg-green-400 disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-1"
                    >
                      {downloadingId === m.material_id ? (
                        <>
                          <Spinner /> Downloading…
                        </>
                      ) : (
                        "Download"
                      )}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        searched && <p className="mt-6 text-gray-400">No materials found.</p>
      )}
    </div>
  );
}
