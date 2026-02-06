import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.config?.url, error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// Companies API
export const companiesAPI = {
  create: (data: any) => apiClient.post('/companies/', data),
  getById: (id: number) => apiClient.get(`/companies/${id}`),
  list: (skip = 0, limit = 100) => apiClient.get(`/companies/?skip=${skip}&limit=${limit}`),
  update: (id: number, data: any) => apiClient.put(`/companies/${id}`, data),
  delete: (id: number) => apiClient.delete(`/companies/${id}`),
};

// Documents API
export const documentsAPI = {
  upload: (companyId: number, documentType: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post(`/documents/upload/${companyId}?document_type=${documentType}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  process: (documentId: number) => apiClient.post(`/documents/process/${documentId}`),
  getByCompany: (companyId: number) => apiClient.get(`/documents/company/${companyId}`),
  getById: (id: number) => apiClient.get(`/documents/${id}`),
  delete: (id: number) => apiClient.delete(`/documents/${id}`),
};

// Assessments API
export const assessmentsAPI = {
  generate: (data: { company_id: number; language?: string }) => 
    apiClient.post('/assessments/generate', data),
  getByCompany: (companyId: number, limit = 10) => 
    apiClient.get(`/assessments/company/${companyId}?limit=${limit}`),
  getById: (id: number) => apiClient.get(`/assessments/${id}`),
  calculateMetrics: (companyId: number, data: any) => 
    apiClient.post(`/assessments/calculate-metrics/${companyId}`, null, { params: data }),
};

// Health Check API
export const healthAPI = {
  ping: () => apiClient.get('/health/ping'),
  status: () => apiClient.get('/health/status'),
};

export default apiClient;
