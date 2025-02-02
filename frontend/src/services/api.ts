import axios from 'axios';
import { ServiceConnection } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with base configuration
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Service map API methods
export const serviceMapApi = {
  async getServiceMap(minScore: number = 0.1): Promise<ServiceConnection[]> {
    try {
      const response = await axiosInstance.get(`/service-map?min_score=${minScore}`);
      return response.data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unknown error occurred');
    }
  },

  async updateTraffic(trafficData: any): Promise<any> {
    const response = await axiosInstance.post('/traffic', trafficData);
    return response.data;
  },

  async updateTrafficBatch(trafficBatch: any[]): Promise<any> {
    const response = await axiosInstance.post('/traffic/batch', trafficBatch);
    return response.data;
  },

  async updateServiceRegistry(registry: Record<string, string>): Promise<any> {
    const response = await axiosInstance.post('/service-registry', registry);
    return response.data;
  },
};