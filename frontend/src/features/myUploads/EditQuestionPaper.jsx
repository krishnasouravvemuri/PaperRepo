"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { listMyQuestionPapers, updateQuestionPaper } from "../../api/questionPapers.js";
import { useToast } from "../../context/ToastContext.jsx";
import {
  FormCard,
  Input,
  Select,
  SubmitButton,
  EXAM_TYPES,
  EXAM_SLOTS,
  SEMESTERS,
} from "../../components/FormControls.jsx";

export default function EditQuestionPaper() {
  const { id } = useParams();
  const router = useRouter();
  const { notify } = useToast();
  const [form, setForm] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    listMyQuestionPapers()
      .then((rows) => {
        const p = (rows || []).find((x) => x.question_paper_id === id);
        if (!p) {
          notify("Not found.", "error");
          router.push("/my-uploads");
          return;
        }
        setForm({
          question_paper_title: p.question_paper_title,
          subject_code: p.subject_code,
          subject_name: p.subject_name,
          question_paper_exam_slot: p.question_paper_exam_slot,
          question_paper_exam_type: p.question_paper_exam_type,
          question_paper_semester: p.question_paper_semester,
          question_paper_year: p.question_paper_year,
        });
      })
      .catch((err) => notify(err.message || "Failed to load.", "error"));
  }, [id]);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await updateQuestionPaper(id, form);
      notify("Updated successfully!", "success");
      router.push("/my-uploads");
    } catch (err) {
      notify(err.message || "Update failed.", "error");
    } finally {
      setBusy(false);
    }
  };

  if (!form) return <p className="text-center text-gray-400 mt-10">Loading…</p>;

  return (
    <FormCard title="Edit Question Paper" onSubmit={onSubmit}>
      <Input label="Title" value={form.question_paper_title} onChange={set("question_paper_title")} required />
      <Input label="Subject Code" value={form.subject_code} onChange={set("subject_code")} required />
      <Input label="Subject Name" value={form.subject_name} onChange={set("subject_name")} required />
      <Select label="Exam Slot" options={EXAM_SLOTS} value={form.question_paper_exam_slot} onChange={set("question_paper_exam_slot")} required />
      <Select label="Exam Type" options={EXAM_TYPES} value={form.question_paper_exam_type} onChange={set("question_paper_exam_type")} required />
      <Select label="Semester" options={SEMESTERS} value={form.question_paper_semester} onChange={set("question_paper_semester")} required />
      <Input label="Year" type="number" value={form.question_paper_year} onChange={set("question_paper_year")} required />
      <SubmitButton busy={busy}>Save changes</SubmitButton>
    </FormCard>
  );
}
