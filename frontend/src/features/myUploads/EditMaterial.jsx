"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { listMyMaterials, updateMaterial } from "../../api/materials.js";
import { useToast } from "../../context/ToastContext.jsx";
import { FormCard, Input, SubmitButton } from "../../components/FormControls.jsx";

export default function EditMaterial() {
  const { id } = useParams();
  const router = useRouter();
  const { notify } = useToast();
  const [form, setForm] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    listMyMaterials()
      .then((rows) => {
        const m = (rows || []).find((x) => x.material_id === id);
        if (!m) {
          notify("Not found.", "error");
          router.push("/my-uploads");
          return;
        }
        setForm({
          material_title: m.material_title,
          subject_code: m.subject_code,
          subject_name: m.subject_name,
          material_topic_type: m.material_topic_type,
          faculty_name: m.faculty_name || "",
        });
      })
      .catch((err) => notify(err.message || "Failed to load.", "error"));
  }, [id]);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await updateMaterial(id, form);
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
    <FormCard title="Edit Study Material" onSubmit={onSubmit}>
      <Input label="Title" value={form.material_title} onChange={set("material_title")} required />
      <Input label="Subject Code" value={form.subject_code} onChange={set("subject_code")} required />
      <Input label="Subject Name" value={form.subject_name} onChange={set("subject_name")} required />
      <Input label="Topic Type" value={form.material_topic_type} onChange={set("material_topic_type")} required />
      <Input label="Faculty Name (optional)" value={form.faculty_name} onChange={set("faculty_name")} />
      <SubmitButton busy={busy}>Save changes</SubmitButton>
    </FormCard>
  );
}
