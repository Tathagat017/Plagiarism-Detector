// API Request and Response Types
export interface AnalyzeRequest {
  texts: string[];
  model_key?: string;
  threshold?: number;
}

export interface SimilarityPair {
  index_1: number;
  index_2: number;
  similarity: number;
  text_1_preview: string;
  text_2_preview: string;
}

export interface AnalyzeResponse {
  similarity_matrix: number[][];
  plagiarized_pairs: SimilarityPair[];
  model_used: string;
  threshold_used: number;
  total_comparisons: number;
  execution_time: number;
}

export interface ModelDescription {
  name: string;
  description: string;
  dimensions: number;
  loaded: boolean;
}

export interface ModelsResponse {
  available_models: string[];
  default_model: string;
  model_descriptions: Record<string, ModelDescription>;
}

export interface HealthResponse {
  status: string;
  version: string;
  models_loaded: boolean;
}

// UI State Types
export interface TextInput {
  id: string;
  content: string;
  label: string;
}

export interface AnalysisState {
  isLoading: boolean;
  result: AnalyzeResponse | null;
  error: string | null;
}

export interface AppState {
  texts: TextInput[];
  selectedModel: string;
  threshold: number;
  analysis: AnalysisState;
  availableModels: ModelsResponse | null;
}
