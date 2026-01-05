import { useState, useCallback, useEffect } from 'react';
import { chatService } from '@/services/chatService';
import { conversationService } from '@/services/conversationService';
import { Message, ChatState } from '@/types/chat';
import { useAuth } from '@/lib/auth-client';

export function useChat() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversations, setConversations] = useState<any[]>([]);

  const loadConversation = useCallback(async (id: number) => {
    if (!user?.id) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const history = await conversationService.getConversationHistory(user.id, id);

      // Handle both array and object responses
      const messagesArray = Array.isArray(history) ? history : (history as any)?.messages || [];

      // Convert API response to our Message format
      const chatMessages: Message[] = messagesArray.map((msg: any) => ({
        id: msg.id.toString(),
        role: msg.role,
        content: msg.content,
        tool_calls: msg.tool_calls,
        timestamp: new Date(msg.created_at),
      }));

      setMessages(chatMessages);
      setConversationId(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  }, [user?.id]);

  const sendMessage = useCallback(async (content: string) => {
    if (!user?.id) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    // Add optimistic user message immediately
    const optimisticUserMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, optimisticUserMessage]);

    try {
      // Set up timeout promise
      const timeoutPromise = new Promise<never>((_, reject) => {
        setTimeout(() => {
          reject(new Error('Request timed out. Please try again.'));
        }, 30000); // 30 second timeout
      });

      // Race the actual API call with the timeout
      const response = await Promise.race([
        chatService.sendMessage(user.id, {
          conversation_id: conversationId || undefined,
          message: content,
        }),
        timeoutPromise
      ]);

      // Add assistant response
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Update conversation ID if new
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }
    } catch (err) {
      if (err instanceof Error && err.message.includes('timed out')) {
        setError('Request timed out. Please try again.');
      } else {
        setError(err instanceof Error ? err.message : 'Failed to send message');
      }
    } finally {
      setIsLoading(false);
    }
  }, [user?.id, conversationId]);

  const startNewConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }, []);

  const loadConversations = useCallback(async () => {
    if (!user?.id) {
      setError('User not authenticated');
      return;
    }

    try {
      const convs = await conversationService.getConversations(user.id);
      setConversations(convs);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversations');
    }
  }, [user?.id]);

  useEffect(() => {
    if (user?.id) {
      loadConversations();
    }
  }, [user?.id, loadConversations]);

  return {
    messages,
    sendMessage,
    isLoading,
    error,
    conversationId,
    startNewConversation,
    loadConversation,
    loadConversations,
    conversations,
  };
}