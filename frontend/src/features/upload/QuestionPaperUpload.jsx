"use client";

import { useState } from "react";
import { uploadQuestionPapers } from "../../api/questionPapers.js";
import { useToast } from "../../context/ToastContext.jsx";
import {
  FormCard,
  Input,
  Select,
  FileInput,
  SubmitButton,
  EXAM_TYPES,
  SEMESTERS,
} from "../../components/FormControls.jsx";

const EMPTY = {
  question_paper_title: "",
  subject_code: "",
  subject_name: "",
  question_paper_exam_slot: "",
  question_paper_exam_type: "",
  question_paper_semester: "",
  question_paper_year: "",
};

export default function QuestionPaperUpload() {
  const { notify } = useToast();
  const [form, setForm] = useState(EMPTY);
  const [files, setFiles] = useState([]);
  const [busy, setBusy] = useState(false);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!files.length) return notify("Choose at least one file.", "warning");
    setBusy(true);
    try {
      const data = await uploadQuestionPapers(form, files);
      notify(`${data?.created_ids?.length || 0} file(s) uploaded!`, "success");
      setForm(EMPTY);
      setFiles([]);
      e.target.reset();
    } catch (err) {
      notify(err.message || "Upload failed.", "error");
    } finally {
      setBusy(false);
    }
  };

  return (
    <FormCard title="Upload Question Papers" onSubmit={onSubmit}>
      <Input label="Title" value={form.question_paper_title} onChange={set("question_paper_title")} required />
      <Input label="Subject Code" value={form.subject_code} onChange={set("subject_code")} required />
      <Input label="Subject Name" value={form.subject_name} onChange={set("subject_name")} required />
      <Input label="Exam Slot" value={form.question_paper_exam_slot} onChange={set("question_paper_exam_slot")} required />
      <Select label="Exam Type" options={EXAM_TYPES} value={form.question_paper_exam_type} onChange={set("question_paper_exam_type")} required />
      <Select label="Semester" options={SEMESTERS} value={form.question_paper_semester} onChange={set("question_paper_semester")} required />
      <Input label="Year" type="number" value={form.question_paper_year} onChange={set("question_paper_year")} required />
      <FileInput label="Files" multiple onChange={(e) => setFiles([...e.target.files])} />
      <SubmitButton busy={busy}>Upload</SubmitButton>
    </FormCard>
  );
}
