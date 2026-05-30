"use client";

import { useState } from "react";
import { uploadMaterials } from "../../api/materials.js";
import { useToast } from "../../context/ToastContext.jsx";
import { FormCard, Input, FileInput, SubmitButton } from "../../components/FormControls.jsx";

const EMPTY = {
  material_title: "",
  subject_code: "",
  subject_name: "",
  material_topic_type: "",
  faculty_name: "",
};

export default function MaterialUpload() {
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
      const data = await uploadMaterials(form, files);
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
    <FormCard title="Upload Study Materials" onSubmit={onSubmit}>
      <Input label="Title" value={form.material_title} onChange={set("material_title")} required />
      <Input label="Subject Code" value={form.subject_code} onChange={set("subject_code")} required />
      <Input label="Subject Name" value={form.subject_name} onChange={set("subject_name")} required />
      <Input label="Topic Type" value={form.material_topic_type} onChange={set("material_topic_type")} required />
      <Input label="Faculty Name (optional)" value={form.faculty_name} onChange={set("faculty_name")} />
      <FileInput label="Files" multiple onChange={(e) => setFiles([...e.target.files])} />
      <SubmitButton busy={busy}>Upload</SubmitButton>
    </FormCard>
  );
}
