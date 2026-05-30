import api from "./client.js";

export const signup = (payload) => api.post("/user_management/signup", payload);
export const login = (payload) => api.post("/user_management/login", payload);
export const logout = () => api.post("/user_management/logout");
export const fetchMe = () => api.get("/user_management/me");
