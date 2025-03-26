// src/axios.js
import axios from "axios";

// ✅ Create Axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // Backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // ✅ Get token from localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // ✅ Add token to headers if available
    }
    return config;
  },
  (error) => {
    return Promise.reject(error); // ❌ Handle error
  }
);

// ✅ Export the configured Axios instance
export default api;
