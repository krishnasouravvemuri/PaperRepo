import api from "./client.js";

const BASE = "/important_topic_management";

export const listImportantTopics = (params) => api.get(`${BASE}/`, { params });
export const listMyImportantTopics = () => api.get(`${BASE}/my_uploads/`);
export const getImportantTopicFileUrl = (id) => api.get(`${BASE}/${id}/file/`);
export const updateImportantTopic = (id, payload) => api.patch(`${BASE}/${id}/`, payload);
export const deleteImportantTopic = (id) => api.delete(`${BASE}/${id}/`);

export const uploadImportantTopics = (fields, files) => {
  const fd = new FormData();
  Object.entries(fields).forEach(([k, v]) => fd.append(k, v));
  files.forEach((f) => fd.append("files", f));
  return api.post(`${BASE}/`, fd);
};
