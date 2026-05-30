"use client";

import { useState } from "react";
import { uploadImportantTopics } from "../../api/importantTopics.js";
import { useToast } from "../../context/ToastContext.jsx";
import {
  FormCard,
  Input,
  Select,
  FileInput,
  SubmitButton,
  EXAM_TYPES,
} from "../../components/FormControls.jsx";

const EMPTY = {
  important_topic_title: "",
  subject_code: "",
  subject_name: "",
  important_topic_exam_type: "",
  faculty_name: "",
};

export default function ImportantTopicUpload() {
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
      const data = await uploadImportantTopics(form, files);
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
    <FormCard title="Upload Important Topics" onSubmit={onSubmit}>
      <Input label="Title" value={form.important_topic_title} onChange={set("important_topic_title")} required />
      <Input label="Subject Code" value={form.subject_code} onChange={set("subject_code")} required />
      <Input label="Subject Name" value={form.subject_name} onChange={set("subject_name")} required />
      <Select label="Exam Type" options={EXAM_TYPES} value={form.important_topic_exam_type} onChange={set("important_topic_exam_type")} required />
      <Input label="Faculty Name (optional)" value={form.faculty_name} onChange={set("faculty_name")} />
      <FileInput label="Files" multiple onChange={(e) => setFiles([...e.target.files])} />
      <SubmitButton busy={busy}>Upload</SubmitButton>
    </FormCard>
  );
}
