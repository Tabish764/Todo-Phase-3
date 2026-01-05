import { chatService } from './chatService';

export class ConversationService {
  async getConversations(userId: string) {
    return await chatService.getConversations(userId);
  }

  async getConversationHistory(userId: string, conversationId: number) {
    return await chatService.getConversationHistory(userId, conversationId);
  }

  async createConversation(userId: string, firstMessage: string) {
    // This would use chatService.sendMessage with no conversation_id to create a new one
    return await chatService.sendMessage(userId, {
      message: firstMessage,
    });
  }
}

export const conversationService = new ConversationService();