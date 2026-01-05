'use client';

import { useAuth } from '@/lib/auth-client';
import { useChat } from '@/hooks/useChat';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import ChatKitWrapper from '@/components/Chat/ChatKitWrapper';
import ConversationSidebar from '@/components/Chat/ConversationSidebar';

// Simple error boundary component
const ErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [hasError, setHasError] = useState(false);

  if (hasError) {
    return (
      <div className="flex items-center justify-center h-full bg-black">
        <div className="text-center">
          <h2 className="text-xl font-bold text-gray-200 mb-2">Something went wrong</h2>
          <p className="text-gray-400 mb-4">Please refresh the page to try again.</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-gray-800 text-gray-100 rounded hover:bg-gray-700 transition-colors border border-gray-700"
          >
            Refresh Page
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

export default function ChatPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const chat = useChat();

  // Get conversation ID from URL parameter
  const urlConversationId = searchParams.get('conversation_id');
  const conversationIdFromUrl = urlConversationId ? parseInt(urlConversationId, 10) : null;

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  // Load conversation from URL parameter if provided and different from current
  useEffect(() => {
    if (user && conversationIdFromUrl && conversationIdFromUrl !== chat.conversationId) {
      chat.loadConversation(conversationIdFromUrl);
    }
  }, [user, conversationIdFromUrl, chat.conversationId, chat.loadConversation]);

  if (authLoading) {
    return <div className="flex items-center justify-center h-screen bg-black text-gray-100">Loading...</div>;
  }

  if (!user) {
    return null; // Will redirect
  }

  return (
    <ErrorBoundary>
      <div className="flex h-screen bg-black">
        <ConversationSidebar
          userId={user.id}
          currentConversationId={chat.conversationId}
          onSelectConversation={(id) => {
            // Load conversation history and update URL
            chat.loadConversation(id);
            router.push(`/chat?conversation_id=${id}`);
          }}
          onNewConversation={() => {
            chat.startNewConversation();
            router.push('/chat');
          }}
        />
        <div className="flex-1 flex flex-col md:ml-0 bg-black">
          <ChatKitWrapper
            messages={chat.messages}
            onSendMessage={chat.sendMessage}
            isLoading={chat.isLoading}
            error={chat.error}
          />
        </div>
      </div>
    </ErrorBoundary>
  );
}