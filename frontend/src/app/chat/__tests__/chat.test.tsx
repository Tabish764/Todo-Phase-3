import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import ChatPage from '@/app/chat/page';
import { useAuth } from '@/lib/auth-client';
import { useChat } from '@/hooks/useChat';
import { chatService } from '@/services/chatService';

// Mock the dependencies
vi.mock('@/lib/auth-client');
vi.mock('@/hooks/useChat');
vi.mock('@/services/chatService');

const mockUseAuth = useAuth as jest.MockedFunction<typeof useAuth>;
const mockUseChat = useChat as jest.MockedFunction<typeof useChat>;
const mockChatService = chatService as jest.Mocked<typeof chatService>;

describe('ChatPage Integration', () => {
  const mockUserId = 'test-user-id';
  const mockUser = { id: mockUserId, email: 'test@example.com' };

  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks();

    // Mock auth to return a user
    mockUseAuth.mockReturnValue({
      user: mockUser,
      loading: false,
    } as any);

    // Mock chat hook
    mockUseChat.mockReturnValue({
      messages: [],
      sendMessage: vi.fn(),
      isLoading: false,
      error: null,
      conversationId: null,
      startNewConversation: vi.fn(),
      loadConversation: vi.fn(),
      loadConversations: vi.fn(),
      conversations: [],
    });
  });

  it('renders chat interface when user is authenticated', () => {
    render(<ChatPage />);

    // Check that the chat interface is rendered
    expect(screen.getByRole('main')).toBeInTheDocument();
  });

  it('shows loading state when user is loading', () => {
    mockUseAuth.mockReturnValue({
      user: null,
      loading: true,
    } as any);

    render(<ChatPage />);

    // Should show loading indicator
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('redirects when user is not authenticated', () => {
    mockUseAuth.mockReturnValue({
      user: null,
      loading: false,
    } as any);

    render(<ChatPage />);

    // Should not render the chat interface when not authenticated
    expect(screen.queryByRole('main')).not.toBeInTheDocument();
  });

  it('allows sending messages', async () => {
    const mockSendMessage = vi.fn();
    const mockMessages = [
      { id: '1', role: 'user', content: 'Hello', timestamp: new Date() },
      { id: '2', role: 'assistant', content: 'Hi there!', timestamp: new Date() },
    ];

    mockUseChat.mockReturnValue({
      messages: mockMessages,
      sendMessage: mockSendMessage,
      isLoading: false,
      error: null,
      conversationId: 123,
      startNewConversation: vi.fn(),
      loadConversation: vi.fn(),
      loadConversations: vi.fn(),
      conversations: [],
    });

    render(<ChatPage />);

    // Find the input field and send a message
    const input = screen.getByRole('textbox');
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Verify that sendMessage was called
    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith('Test message');
    });
  });

  it('displays messages correctly', () => {
    const mockMessages = [
      { id: '1', role: 'user', content: 'Hello', timestamp: new Date() },
      { id: '2', role: 'assistant', content: 'Hi there!', timestamp: new Date() },
    ];

    mockUseChat.mockReturnValue({
      messages: mockMessages,
      sendMessage: vi.fn(),
      isLoading: false,
      error: null,
      conversationId: 123,
      startNewConversation: vi.fn(),
      loadConversation: vi.fn(),
      loadConversations: vi.fn(),
      conversations: [],
    });

    render(<ChatPage />);

    // Check that messages are displayed
    expect(screen.getByText('Hello')).toBeInTheDocument();
    expect(screen.getByText('Hi there!')).toBeInTheDocument();
  });

  it('shows loading indicator when sending message', () => {
    mockUseChat.mockReturnValue({
      messages: [],
      sendMessage: vi.fn(),
      isLoading: true,
      error: null,
      conversationId: 123,
      startNewConversation: vi.fn(),
      loadConversation: vi.fn(),
      loadConversations: vi.fn(),
      conversations: [],
    });

    render(<ChatPage />);

    // Check for loading indicator
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays error messages', () => {
    const errorMessage = 'Failed to send message';

    mockUseChat.mockReturnValue({
      messages: [],
      sendMessage: vi.fn(),
      isLoading: false,
      error: errorMessage,
      conversationId: 123,
      startNewConversation: vi.fn(),
      loadConversation: vi.fn(),
      loadConversations: vi.fn(),
      conversations: [],
    });

    render(<ChatPage />);

    // Check that error message is displayed
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });
});