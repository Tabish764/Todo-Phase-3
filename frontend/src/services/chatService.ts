import { apiClient } from '@/lib/api';
import { ChatRequest, ChatResponse } from '@/types/chat';

export class ChatService {
  async sendMessage(
    userId: string,
    request: ChatRequest
  ): Promise<ChatResponse> {
    try {
      const response = await apiClient.request<ChatResponse>(`/api/${userId}/chat`, {
        method: 'POST',
        body: JSON.stringify(request),
      });

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to send message');
      }

      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getConversations(userId: string): Promise<any[]> {
    try {
      const response = await apiClient.getConversations(userId);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to get conversations');
      }

      return response.data.conversations || response.data || [];
    } catch (error) {
      console.error('Error getting conversations:', error);
      throw error;
    }
  }

  async getConversationHistory(
    userId: string,
    conversationId: number
  ): Promise<any[]> {
    try {
      const response = await apiClient.request<any[]>(`/${userId}/conversations/${conversationId}/messages`);

      if (!response.success || !response.data) {
        throw new Error(response.error || 'Failed to get conversation history');
      }

      return response.data;
    } catch (error) {
      console.error('Error getting conversation history:', error);
      throw error;
    }
  }
}

export const chatService = new ChatService();