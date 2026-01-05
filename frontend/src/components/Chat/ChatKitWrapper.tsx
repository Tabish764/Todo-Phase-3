'use client';

import React, { useState } from 'react';
import { Message } from '@/types/chat';
import { ToolCallDisplay } from './ToolCallDisplay';
import { ErrorDisplay } from './ErrorDisplay';

interface ChatKitWrapperProps {
  messages: Message[];
  onSendMessage: (content: string) => void;
  isLoading: boolean;
  error: string | null;
}

const ChatKitWrapper: React.FC<ChatKitWrapperProps> = ({
  messages,
  onSendMessage,
  isLoading,
  error
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    onSendMessage(inputValue);
    setInputValue('');
  };

  return (
    <div className="flex flex-col h-full bg-black text-gray-100">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`p-3 rounded-lg max-w-full sm:max-w-4xl ${
              message.role === 'user'
                ? 'bg-gray-900 ml-auto text-right border border-gray-800'
                : 'bg-gray-950 mr-auto text-left border border-gray-800'
            }`}
          >
            <div className="text-xs text-gray-500 mb-1.5 font-medium">
              {message.role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div className="whitespace-pre-wrap break-words text-gray-100 leading-relaxed">{message.content}</div>

            {/* Display tool calls if they exist */}
            {message.tool_calls && message.tool_calls.length > 0 && (
              <div className="mt-2">
                {message.tool_calls.map((toolCall, index) => (
                  <ToolCallDisplay key={index} toolCall={toolCall} />
                ))}
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="p-3 rounded-lg bg-gray-950 mr-auto text-left border border-gray-800 max-w-full sm:max-w-4xl">
            <div className="text-xs text-gray-500 mb-1.5 font-medium">Assistant</div>
            <div className="text-gray-400">Thinking...</div>
          </div>
        )}
      </div>

      {/* Error display */}
      {error && <ErrorDisplay error={error} />}

      {/* Input form */}
      <div className="p-4 border-t border-gray-800 bg-black">
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2">
          <input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-3 bg-gray-900 border border-gray-800 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-gray-700 focus:ring-1 focus:ring-gray-700 mb-2 sm:mb-0"
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e as any);
              }
            }}
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="p-3 bg-gray-800 text-gray-100 rounded-lg hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors border border-gray-700"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatKitWrapper;