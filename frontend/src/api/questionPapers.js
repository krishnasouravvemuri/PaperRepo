import api from "./client.js";

const BASE = "/question_paper_management";

export const listQuestionPapers = (params) => api.get(`${BASE}/`, { params });
export const listMyQuestionPapers = () => api.get(`${BASE}/my_uploads/`);
export const getQuestionPaperFileUrl = (id) => api.get(`${BASE}/${id}/file/`);
export const updateQuestionPaper = (id, payload) => api.patch(`${BASE}/${id}/`, payload);
export const deleteQuestionPaper = (id) => api.delete(`${BASE}/${id}/`);

export const uploadQuestionPapers = (fields, files) => {
  const fd = new FormData();
  Object.entries(fields).forEach(([k, v]) => fd.append(k, v));
  files.forEach((f) => fd.append("files", f));
  return api.post(`${BASE}/`, fd);
};
