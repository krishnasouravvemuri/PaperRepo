import api from "./client.js";

const BASE = "/material_management";

export const listMaterials = (params) => api.get(`${BASE}/`, { params });
export const listMyMaterials = () => api.get(`${BASE}/my_uploads/`);
export const getMaterialFileUrl = (id) => api.get(`${BASE}/${id}/file/`);
export const updateMaterial = (id, payload) => api.patch(`${BASE}/${id}/`, payload);
export const deleteMaterial = (id) => api.delete(`${BASE}/${id}/`);

export const uploadMaterials = (fields, files) => {
  const fd = new FormData();
  Object.entries(fields).forEach(([k, v]) => fd.append(k, v));
  files.forEach((f) => fd.append("files", f));
  return api.post(`${BASE}/`, fd);
};
