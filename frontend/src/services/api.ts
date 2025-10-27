/**
 * API服务
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5分钟超时
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等认证信息
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // 服务器返回错误
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // 请求发送但没有收到响应
      console.error('Network Error:', error.request);
    } else {
      // 其他错误
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export interface DatasetInfo {
  id: string;
  filename: string;
  format: string;
  upload_time: string;
  rows: number;
  columns: number;
  column_names: string[];
  data_types: Record<string, string>;
  description?: string;
}

export interface ChartConfig {
  type: string;
  title: string;
  data: any;
  config?: any;
}

export interface AnalysisResult {
  analysis_id: string;
  dataset_id: string;
  summary: string;
  insights: string[];
  charts: ChartConfig[];
  statistics: any;
  created_at: string;
}

export interface PredictionResult {
  prediction_id: string;
  dataset_id: string;
  model_name: string;
  predictions: number[];
  confidence_intervals?: Array<{ lower: number; upper: number }>;
  metrics: Record<string, number>;
  validation_passed: boolean;
  validation_details: any;
  chart: ChartConfig;
  created_at: string;
}

export interface WorkRecord {
  record_id: string;
  user_id: string;
  title: string;
  type: string;
  dataset_name: string;
  description: string;
  thumbnail?: string;
  created_at: string;
  updated_at: string;
  result_id: string;
}

// Dataset API
export const uploadDataset = async (file: File, description?: string): Promise<DatasetInfo> => {
  const formData = new FormData();
  formData.append('file', file);
  if (description) {
    formData.append('description', description);
  }

  const response = await api.post('/api/upload/dataset', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getDatasetInfo = async (datasetId: string): Promise<DatasetInfo> => {
  const response = await api.get(`/api/upload/dataset/${datasetId}`);
  return response.data;
};

export const getDatasetPreview = async (datasetId: string, rows: number = 10): Promise<any> => {
  const response = await api.get(`/api/upload/dataset/${datasetId}/preview?rows=${rows}`);
  return response.data;
};

// Analysis API
export const analyzeData = async (
  datasetId: string,
  userQuery: string,
  dataDescription?: string
): Promise<AnalysisResult> => {
  const response = await api.post('/api/analysis/analyze', {
    dataset_id: datasetId,
    user_query: userQuery,
    data_description: dataDescription,
  });
  return response.data;
};

export const getAnalysisResult = async (analysisId: string): Promise<AnalysisResult> => {
  const response = await api.get(`/api/analysis/result/${analysisId}`);
  return response.data;
};

// Prediction API
export const predictData = async (
  datasetId: string,
  targetColumn: string,
  predictionQuery: string,
  modelType?: string,
  forecastPeriods?: number
): Promise<PredictionResult> => {
  const response = await api.post('/api/prediction/predict', {
    dataset_id: datasetId,
    target_column: targetColumn,
    prediction_query: predictionQuery,
    model_type: modelType,
    forecast_periods: forecastPeriods,
  });
  return response.data;
};

export const getPredictionResult = async (predictionId: string): Promise<PredictionResult> => {
  const response = await api.get(`/api/prediction/result/${predictionId}`);
  return response.data;
};

export const validateTimeSeries = async (
  datasetId: string,
  column: string
): Promise<any> => {
  const response = await api.post(`/api/prediction/validate/${datasetId}?column=${column}`);
  return response.data;
};

// User API
export const registerUser = async (username: string, email?: string): Promise<any> => {
  const response = await api.post(`/api/user/register?username=${username}&email=${email || ''}`);
  return response.data;
};

export const getUserInfo = async (userId: string): Promise<any> => {
  const response = await api.get(`/api/user/info/${userId}`);
  return response.data;
};

export const getWorkRecords = async (userId: string): Promise<WorkRecord[]> => {
  const response = await api.get(`/api/user/records/${userId}`);
  return response.data;
};

export const addWorkRecord = async (userId: string, record: Partial<WorkRecord>): Promise<any> => {
  const response = await api.post(`/api/user/records/${userId}`, record);
  return response.data;
};

export const deleteWorkRecord = async (userId: string, recordId: string): Promise<any> => {
  const response = await api.delete(`/api/user/records/${userId}/${recordId}`);
  return response.data;
};

export default api;

