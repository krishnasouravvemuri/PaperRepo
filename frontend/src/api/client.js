import axios from "axios";

const api = axios.create({
  baseURL: "/api/v2",
  withCredentials: true,
});

// Unwrap {meta, data}; surface meta.message on errors.
api.interceptors.response.use(
  (response) => {
    console.log("BACKEND RESPONSE", response.data);
    return response.data?.data;
  },
  (error) => {
    console.log("BACKEND RESPONSE", error.response?.data ?? error);
    const meta = error.response?.data?.meta;
    const message = meta?.message || error.message || "Request failed.";
    return Promise.reject({ status: error.response?.status, message, data: error.response?.data?.data });
  }
);

export default api;
