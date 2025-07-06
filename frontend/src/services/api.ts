import axios from "axios";
import type {
  AnalyzeRequest,
  AnalyzeResponse,
  ModelsResponse,
  HealthResponse,
} from "../types/api";

const API_BASE_URL = "http://localhost:8000/api/v1";

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout for analysis requests
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error("API Response Error:", error);
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.detail || "Server error occurred");
    } else if (error.request) {
      // Request was made but no response received
      throw new Error(
        "Unable to connect to the server. Please check if the backend is running."
      );
    } else {
      // Something else happened
      throw new Error("An unexpected error occurred");
    }
  }
);

export const apiService = {
  // Analyze texts for plagiarism
  async analyzePlagiarism(request: AnalyzeRequest): Promise<AnalyzeResponse> {
    const response = await apiClient.post<AnalyzeResponse>("/analyze", request);
    return response.data;
  },

  // Get available models
  async getAvailableModels(): Promise<ModelsResponse> {
    const response = await apiClient.get<ModelsResponse>("/models");
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>("/health");
    return response.data;
  },

  // Compare two specific texts
  async compareTwoTexts(
    text1: string,
    text2: string,
    modelKey: string = "miniLM"
  ): Promise<unknown> {
    const response = await apiClient.post("/compare", null, {
      params: { text1, text2, model_key: modelKey },
    });
    return response.data;
  },

  // Get detailed analysis
  async getDetailedAnalysis(request: AnalyzeRequest): Promise<unknown> {
    const response = await apiClient.post("/analyze/detailed", request);
    return response.data;
  },
};

export default apiService;
