"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { listMyImportantTopics, updateImportantTopic } from "../../api/importantTopics.js";
import { useToast } from "../../context/ToastContext.jsx";
import { FormCard, Input, Select, SubmitButton, EXAM_TYPES } from "../../components/FormControls.jsx";

export default function EditImportantTopic() {
  const { id } = useParams();
  const router = useRouter();
  const { notify } = useToast();
  const [form, setForm] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    listMyImportantTopics()
      .then((rows) => {
        const t = (rows || []).find((x) => x.important_topic_id === id);
        if (!t) {
          notify("Not found.", "error");
          router.push("/my-uploads");
          return;
        }
        setForm({
          important_topic_title: t.important_topic_title,
          subject_code: t.subject_code,
          subject_name: t.subject_name,
          important_topic_exam_type: t.important_topic_exam_type,
          faculty_name: t.faculty_name || "",
        });
      })
      .catch((err) => notify(err.message || "Failed to load.", "error"));
  }, [id]);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await updateImportantTopic(id, form);
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
    <FormCard title="Edit Important Topic" onSubmit={onSubmit}>
      <Input label="Title" value={form.important_topic_title} onChange={set("important_topic_title")} required />
      <Input label="Subject Code" value={form.subject_code} onChange={set("subject_code")} required />
      <Input label="Subject Name" value={form.subject_name} onChange={set("subject_name")} required />
      <Select label="Exam Type" options={EXAM_TYPES} value={form.important_topic_exam_type} onChange={set("important_topic_exam_type")} required />
      <Input label="Faculty Name (optional)" value={form.faculty_name} onChange={set("faculty_name")} />
      <SubmitButton busy={busy}>Save changes</SubmitButton>
    </FormCard>
  );
}
