export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: Array<{
    tool_name: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
  timestamp: Date;
  isLoading?: boolean;
  error?: string | null;
}

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: Array<{
    tool_name: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
}

export interface ToolCall {
  name: string;
  arguments: Record<string, any>;
  result: Record<string, any>;
}

export interface ChatState {
  currentConversationId: number | null;
  messages: Message[];
  inputText: string;
  isLoading: boolean;
  error: string | null;
  conversations: Conversation[];
  sidebarOpen: boolean;
}

export interface Conversation {
  id: number;
  title: string;
  lastUpdated: Date;
  messageCount: number;
  preview: string;
}

export interface MessageDisplay {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  formattedContent: string;
  isExpanded: boolean;
  isPending: boolean;
}

export interface ConversationListItem {
  id: number;
  title: string;
  lastMessagePreview: string;
  lastUpdated: Date;
  isActive: boolean;
  unreadCount: number;
}