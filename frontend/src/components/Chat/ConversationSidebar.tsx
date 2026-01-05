import React, { useEffect, useState } from 'react';
import { conversationService } from '@/services/conversationService';

interface ConversationSidebarProps {
  userId: string;
  currentConversationId: number | null;
  onSelectConversation: (id: number) => void;
  onNewConversation: () => void;
}

interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

const ConversationSidebar: React.FC<ConversationSidebarProps> = ({
  userId,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false); // For mobile menu toggle

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const convs = await conversationService.getConversations(userId);
        setConversations(convs);
      } catch (error) {
        console.error('Error fetching conversations:', error);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchConversations();
    }
  }, [userId]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <>
      {/* Mobile menu button */}
      <button
        className="md:hidden fixed top-4 left-4 z-50 p-2 bg-gray-900 text-gray-100 rounded-lg border border-gray-800 hover:bg-gray-800 transition-colors"
        onClick={() => setIsOpen(!isOpen)}
      >
        ☰
      </button>

      {/* Sidebar - visible on desktop, overlay on mobile when open */}
      <div
        className={`fixed md:static w-64 bg-black border-r border-gray-800 p-4 flex flex-col h-full z-40 transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } md:translate-x-0`}
      >
        <div className="md:hidden flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-100">Chats</h2>
          <button
            onClick={() => setIsOpen(false)}
            className="text-gray-500 hover:text-gray-300 transition-colors"
          >
            ✕
          </button>
        </div>

        <button
          onClick={onNewConversation}
          className="mb-4 w-full py-2 px-4 bg-gray-900 text-gray-100 rounded-lg hover:bg-gray-800 transition-colors border border-gray-800"
        >
          + New Chat
        </button>

        <div className="flex-1 overflow-y-auto">
          <h3 className="font-semibold text-gray-400 mb-2 hidden md:block text-xs uppercase tracking-wider">Recent Chats</h3>
          {loading ? (
            <div className="text-sm text-gray-500">Loading...</div>
          ) : (
            <ul className="space-y-1">
              {conversations.map((conversation) => (
                <li key={conversation.id}>
                  <button
                    onClick={() => {
                      onSelectConversation(conversation.id);
                      setIsOpen(false); // Close mobile menu after selection
                    }}
                    className={`w-full text-left p-2 rounded-lg transition-colors ${
                      currentConversationId === conversation.id
                        ? 'bg-gray-900 border border-gray-800'
                        : 'hover:bg-gray-900 border border-transparent'
                    }`}
                  >
                    <div className="font-medium truncate text-gray-100 text-sm">{conversation.title}</div>
                    <div className="text-xs text-gray-500 truncate">
                      {formatDate(conversation.updated_at)}
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-80 z-30 md:hidden"
          onClick={() => setIsOpen(false)}
        ></div>
      )}
    </>
  );
};

export default ConversationSidebar;