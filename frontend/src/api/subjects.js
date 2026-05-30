import api from "./client.js";

export const listSubjects = (search) =>
  api.get("/subject_management/", { params: search ? { search } : {} });
