import axios from 'axios';
import { HealthResponse, ChatResponse } from './types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async (): Promise<HealthResponse> => {
  const res = await apiClient.get<HealthResponse>('/health');
  return res.data;
};

export const sendChatMessage = async (question: string, conversationId?: string): Promise<ChatResponse> => {
  const res = await apiClient.post<ChatResponse>('/chat', {
    question,
    conversation_id: conversationId,
  });
  return res.data;
};
