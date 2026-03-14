import api from "@/services/api";
import { AuthResponse, User } from "@/types/user";

export const authService = {
  login: async (formData: FormData): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data;
  },

  register: async (userData: any): Promise<User> => {
    const response = await api.post<User>("/auth/register", userData);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get<User>("/users/me");
    return response.data;
  },

  logout: () => {
    localStorage.removeItem("token");
  },

  getToken: () => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("token");
    }
    return null;
  },

  setToken: (token: string) => {
    localStorage.setItem("token", token);
  },
};
