import axios from "axios";

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(
      `Making ${config.method?.toUpperCase()} request to:`,
      config.url
    );
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Expense API functions
export const expenseAPI = {
  // Get all expenses
  getExpenses: (params = {}) => {
    return api.get("/expenses", { params });
  },

  // Get single expense
  getExpense: (id) => {
    return api.get(`/expenses/${id}`);
  },

  // Create new expense
  createExpense: (expenseData) => {
    return api.post("/expenses", expenseData);
  },

  // Update expense
  updateExpense: (id, expenseData) => {
    return api.put(`/expenses/${id}`, expenseData);
  },

  // Delete expense (soft delete)
  deleteExpense: (id) => {
    return api.delete(`/expenses/${id}`);
  },

  // Restore expense
  restoreExpense: (id) => {
    return api.put(`/expenses/${id}/restore`);
  },

  // Toggle expense done status
  toggleExpenseDone: (id) => {
    return api.put(`/expenses/${id}/toggle-done`);
  },

  // Permanently delete expense
  permanentlyDeleteExpense: (id) => {
    return api.delete(`/expenses/${id}/permanent`);
  },

  // Get trashed expenses
  getTrashedExpenses: () => {
    return api.get("/expenses/trash");
  },
};

// Dashboard API functions
export const dashboardAPI = {
  // Get dashboard summary
  getDashboardSummary: () => {
    return api.get("/dashboard");
  },
};

// Settings API functions
export const settingsAPI = {
  // Get user settings
  getSettings: () => {
    return api.get("/settings");
  },

  // Update user settings
  updateSettings: (settingsData) => {
    return api.put("/settings", settingsData);
  },
};

// Utility API functions
export const utilityAPI = {
  // Get categories and options
  getCategories: () => {
    return api.get("/categories");
  },

  // Health check
  healthCheck: () => {
    return api.get("/health");
  },
};

export default api;
