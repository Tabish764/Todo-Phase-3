import { renderHook, act } from '@testing-library/react';
import { useChat } from '../useChat';
import { chatService } from '@/services/chatService';
import { conversationService } from '@/services/conversationService';
import { useAuth } from '@/lib/auth-client';

// Mock the dependencies
jest.mock('@/lib/auth-client');
jest.mock('@/services/chatService');
jest.mock('@/services/conversationService');

const mockUseAuth = useAuth as jest.MockedFunction<typeof useAuth>;
const mockChatService = chatService as jest.Mocked<typeof chatService>;
const mockConversationService = conversationService as jest.Mocked<typeof conversationService>;

describe('useChat', () => {
  const mockUserId = 'test-user-id';
  const mockUser = { id: mockUserId, email: 'test@example.com' };

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock auth to return a user
    mockUseAuth.mockReturnValue({
      user: mockUser,
      loading: false,
    } as any);
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useChat());

    expect(result.current.messages).toEqual([]);
    expect(result.current.conversationId).toBeNull();
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.conversations).toEqual([]);
  });

  it('should send a message successfully', async () => {
    const mockRequest = {
      conversation_id: 123,
      message: 'Hello, world!',
    };

    const mockResponse = {
      conversation_id: 123,
      response: 'Hello back!',
      tool_calls: [],
    };

    mockChatService.sendMessage.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage('Hello, world!');
    });

    expect(mockChatService.sendMessage).toHaveBeenCalledWith(
      mockUserId,
      mockRequest
    );

    // Check that messages were updated
    expect(result.current.messages).toHaveLength(2);
    expect(result.current.messages[0].role).toBe('user');
    expect(result.current.messages[0].content).toBe('Hello, world!');
    expect(result.current.messages[1].role).toBe('assistant');
    expect(result.current.messages[1].content).toBe('Hello back!');
  });

  it('should start a new conversation', () => {
    const { result } = renderHook(() => useChat());

    // Set some state to verify it gets reset
    act(() => {
      result.current.startNewConversation();
    });

    expect(result.current.messages).toEqual([]);
    expect(result.current.conversationId).toBeNull();
    expect(result.current.error).toBeNull();
  });

  it('should load conversation history', async () => {
    const mockConversationId = 123;
    const mockHistory = [
      { id: '1', role: 'user', content: 'Hello', created_at: '2023-01-01T00:00:00Z' },
      { id: '2', role: 'assistant', content: 'Hi there!', created_at: '2023-01-01T00:00:01Z' },
    ];

    mockConversationService.getConversationHistory.mockResolvedValue(mockHistory);

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.loadConversation(mockConversationId);
    });

    expect(mockConversationService.getConversationHistory).toHaveBeenCalledWith(
      mockUserId,
      mockConversationId
    );

    expect(result.current.messages).toHaveLength(2);
    expect(result.current.conversationId).toBe(mockConversationId);
  });

  it('should load conversations list', async () => {
    const mockConversations = [
      { id: 1, title: 'Conversation 1' },
      { id: 2, title: 'Conversation 2' },
    ];

    mockConversationService.getConversations.mockResolvedValue(mockConversations);

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.loadConversations();
    });

    expect(mockConversationService.getConversations).toHaveBeenCalledWith(mockUserId);
    expect(result.current.conversations).toEqual(mockConversations);
  });

  it('should handle error when user is not authenticated', async () => {
    // Mock auth to return no user
    mockUseAuth.mockReturnValue({
      user: null,
      loading: false,
    } as any);

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage('Hello');
    });

    expect(result.current.error).toBe('User not authenticated');
  });

  it('should handle error when sending message fails', async () => {
    const errorMessage = 'Failed to send message';
    mockChatService.sendMessage.mockRejectedValue(new Error(errorMessage));

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage('Hello, world!');
    });

    expect(result.current.error).toBe(errorMessage);
  });

  it('should handle timeout error', async () => {
    // Mock a timeout by making the API call take longer than the timeout
    mockChatService.sendMessage.mockImplementation(() => {
      return new Promise((_, reject) => {
        setTimeout(() => {
          reject(new Error('Request timed out. Please try again.'));
        }, 35000); // Longer than the 30 second timeout
      });
    });

    const { result } = renderHook(() => useChat());

    await act(async () => {
      await result.current.sendMessage('Hello, world!');
    });

    expect(result.current.error).toBe('Request timed out. Please try again.');
  });
});