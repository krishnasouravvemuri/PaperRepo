import axios from "axios";

const api = axios.create({
  baseURL: "/api/v2",
  withCredentials: true,
});

// Unwrap {meta, data}; surface meta.message on errors.
api.interceptors.response.use(
  (response) => response.data?.data,
  (error) => {
    const meta = error.response?.data?.meta;
    const message = meta?.message || error.message || "Request failed.";
    return Promise.reject({ status: error.response?.status, message, data: error.response?.data?.data });
  }
);

export default api;
