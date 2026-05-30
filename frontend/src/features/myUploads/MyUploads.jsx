"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listMyQuestionPapers, deleteQuestionPaper } from "../../api/questionPapers.js";
import { listMyImportantTopics, deleteImportantTopic } from "../../api/importantTopics.js";
import { listMyMaterials, deleteMaterial } from "../../api/materials.js";
import { useToast } from "../../context/ToastContext.jsx";

function Section({ title, columns, rows, renderRow }) {
  return (
    <div className="mt-8 p-6 bg-[#1e1e2e] rounded-2xl shadow-2xl overflow-x-auto">
      <h2 className="text-2xl font-semibold mb-4 text-teal-400">{title}</h2>
      {rows.length === 0 ? (
        <p className="text-gray-400">Nothing here yet.</p>
      ) : (
        <table className="min-w-full text-left border border-gray-700 rounded-lg">
          <thead className="bg-[#221c35] text-teal-400">
            <tr>
              {columns.map((c) => (
                <th key={c} className="px-4 py-2 border-r border-gray-600">
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>{rows.map(renderRow)}</tbody>
        </table>
      )}
    </div>
  );
}

const actionCell = (editTo, onDelete) => (
  <td className="px-4 py-2 flex gap-2 justify-center">
    <Link href={editTo} className="px-2 py-1 bg-yellow-500 rounded text-black hover:bg-yellow-400">
      Edit
    </Link>
    <button onClick={onDelete} className="px-2 py-1 bg-red-500 rounded text-white hover:bg-red-400">
      Delete
    </button>
  </td>
);

export default function MyUploads() {
  const { notify } = useToast();
  const [qp, setQp] = useState([]);
  const [it, setIt] = useState([]);
  const [mat, setMat] = useState([]);

  const loadAll = async () => {
    try {
      const [a, b, c] = await Promise.all([
        listMyQuestionPapers(),
        listMyImportantTopics(),
        listMyMaterials(),
      ]);
      setQp(a || []);
      setIt(b || []);
      setMat(c || []);
    } catch (err) {
      notify(err.message || "Failed to load.", "error");
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  const del = (fn, id, label) => async () => {
    if (!window.confirm(`Delete this ${label}?`)) return;
    try {
      await fn(id);
      notify(`${label} deleted.`, "success");
      loadAll();
    } catch (err) {
      notify(err.message || "Delete failed.", "error");
    }
  };

  return (
    <div className="mt-6">
      <h1 className="text-3xl font-bold text-teal-400">My Uploads</h1>

      <Section
        title="Question Papers"
        columns={["Title", "Subject", "Code", "Slot", "Exam", "Semester", "Year", "Actions"]}
        rows={qp}
        renderRow={(p) => (
          <tr key={p.question_paper_id} className="border-b border-gray-700 hover:bg-[#2a2235]">
            <td className="px-4 py-2 border-r border-gray-600">{p.question_paper_title}</td>
            <td className="px-4 py-2 border-r border-gray-600">{p.subject_name}</td>
            <td className="px-4 py-2 border-r border-gray-600">{p.subject_code}</td>
            <td className="px-4 py-2 border-r border-gray-600">{p.question_paper_exam_slot}</td>
            <td className="px-4 py-2 border-r border-gray-600">{p.question_paper_exam_type}</td>
            <td className="px-4 py-2 border-r border-gray-600">{p.question_paper_semester}</td>
            <td className="px-4 py-2 border-r border-gray-600">{p.question_paper_year}</td>
            {actionCell(
              `/my-uploads/question-papers/${p.question_paper_id}/edit`,
              del(deleteQuestionPaper, p.question_paper_id, "question paper")
            )}
          </tr>
        )}
      />

      <Section
        title="Important Topics"
        columns={["Title", "Subject", "Code", "Exam", "Faculty", "Actions"]}
        rows={it}
        renderRow={(t) => (
          <tr key={t.important_topic_id} className="border-b border-gray-700 hover:bg-[#2a2235]">
            <td className="px-4 py-2 border-r border-gray-600">{t.important_topic_title}</td>
            <td className="px-4 py-2 border-r border-gray-600">{t.subject_name}</td>
            <td className="px-4 py-2 border-r border-gray-600">{t.subject_code}</td>
            <td className="px-4 py-2 border-r border-gray-600">{t.important_topic_exam_type}</td>
            <td className="px-4 py-2 border-r border-gray-600">{t.faculty_name || "-"}</td>
            {actionCell(
              `/my-uploads/important-topics/${t.important_topic_id}/edit`,
              del(deleteImportantTopic, t.important_topic_id, "important topic")
            )}
          </tr>
        )}
      />

      <Section
        title="Study Materials"
        columns={["Title", "Subject", "Code", "Topic Type", "Faculty", "Actions"]}
        rows={mat}
        renderRow={(m) => (
          <tr key={m.material_id} className="border-b border-gray-700 hover:bg-[#2a2235]">
            <td className="px-4 py-2 border-r border-gray-600">{m.material_title}</td>
            <td className="px-4 py-2 border-r border-gray-600">{m.subject_name}</td>
            <td className="px-4 py-2 border-r border-gray-600">{m.subject_code}</td>
            <td className="px-4 py-2 border-r border-gray-600">{m.material_topic_type}</td>
            <td className="px-4 py-2 border-r border-gray-600">{m.faculty_name || "-"}</td>
            {actionCell(
              `/my-uploads/materials/${m.material_id}/edit`,
              del(deleteMaterial, m.material_id, "material")
            )}
          </tr>
        )}
      />
    </div>
  );
}
