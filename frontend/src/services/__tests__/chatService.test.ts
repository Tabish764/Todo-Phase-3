import { ChatService } from '../chatService';
import { ChatRequest, ChatResponse } from '@/types/chat';

// Mock fetch API
global.fetch = jest.fn();

describe('ChatService', () => {
  let chatService: ChatService;
  const mockUserId = 'test-user-id';
  const mockRequest: ChatRequest = {
    message: 'Hello, world!',
    conversation_id: 123,
  };

  beforeEach(() => {
    chatService = new ChatService();
    (global.fetch as jest.Mock).mockClear();
  });

  describe('sendMessage', () => {
    it('should send a message successfully', async () => {
      // Arrange
      const mockResponse: ChatResponse = {
        conversation_id: 123,
        response: 'Hello back!',
        tool_calls: [],
      };

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockResponse),
      });

      // Act
      const result = await chatService.sendMessage(mockUserId, mockRequest);

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${mockUserId}/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(mockRequest),
        }
      );
      expect(result).toEqual(mockResponse);
    });

    it('should throw an error when API returns non-OK response', async () => {
      // Arrange
      const errorResponse = { message: 'Something went wrong' };

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue(errorResponse),
        status: 500,
      });

      // Act & Assert
      await expect(chatService.sendMessage(mockUserId, mockRequest)).rejects.toThrow(
        errorResponse.message
      );
    });

    it('should handle network errors', async () => {
      // Arrange
      (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

      // Act & Assert
      await expect(chatService.sendMessage(mockUserId, mockRequest)).rejects.toThrow(
        'Network error'
      );
    });

    it('should handle non-JSON error response', async () => {
      // Arrange
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockRejectedValue(new Error('Not JSON')),
        status: 500,
      });

      // Act & Assert
      await expect(chatService.sendMessage(mockUserId, mockRequest)).rejects.toThrow(
        'HTTP error! status: 500'
      );
    });
  });

  describe('getConversations', () => {
    it('should fetch conversations successfully', async () => {
      // Arrange
      const mockConversations = [
        { id: 1, title: 'Conversation 1', lastMessage: 'Hello' },
        { id: 2, title: 'Conversation 2', lastMessage: 'Hi' },
      ];

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockConversations),
      });

      // Act
      const result = await chatService.getConversations(mockUserId);

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${mockUserId}/conversations`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      expect(result).toEqual(mockConversations);
    });

    it('should throw an error when getting conversations fails', async () => {
      // Arrange
      const errorResponse = { message: 'Failed to get conversations' };

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue(errorResponse),
        status: 500,
      });

      // Act & Assert
      await expect(chatService.getConversations(mockUserId)).rejects.toThrow(
        errorResponse.message
      );
    });
  });

  describe('getConversationHistory', () => {
    it('should fetch conversation history successfully', async () => {
      // Arrange
      const mockConversationId = 123;
      const mockHistory = [
        { role: 'user', content: 'Hello' },
        { role: 'assistant', content: 'Hi there!' },
      ];

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockHistory),
      });

      // Act
      const result = await chatService.getConversationHistory(
        mockUserId,
        mockConversationId
      );

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${mockUserId}/conversations/${mockConversationId}/messages`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      expect(result).toEqual(mockHistory);
    });

    it('should throw an error when getting conversation history fails', async () => {
      // Arrange
      const mockConversationId = 123;
      const errorResponse = { message: 'Failed to get history' };

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue(errorResponse),
        status: 500,
      });

      // Act & Assert
      await expect(
        chatService.getConversationHistory(mockUserId, mockConversationId)
      ).rejects.toThrow(errorResponse.message);
    });
  });
});