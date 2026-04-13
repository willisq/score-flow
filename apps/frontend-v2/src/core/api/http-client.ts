import axios from "axios";

export const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ?? "Error inesperado en la comunicación con el servidor.";

    console.error("[HTTP Error]", {
      status: error.response?.status,
      url: error.config?.url,
      message,
    });

    return Promise.reject(error);
  },
);
