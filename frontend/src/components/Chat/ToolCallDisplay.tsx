import React from 'react';

interface ToolCall {
  tool_name: string;
  arguments: Record<string, any>;
  result: Record<string, any>;
}

interface ToolCallDisplayProps {
  toolCall: ToolCall;
}

const ToolCallDisplay: React.FC<ToolCallDisplayProps> = ({ toolCall }) => {
  const [isExpanded, setIsExpanded] = React.useState(false);

  return (
    <div className="mt-2 p-3 bg-gray-900 border border-gray-800 rounded-lg">
      <div
        className="flex justify-between items-center cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="font-semibold text-sm text-gray-300">
          🛠️ {toolCall.tool_name}
        </div>
        <button className="text-gray-500 hover:text-gray-300 transition-colors">
          {isExpanded ? '−' : '+'}
        </button>
      </div>

      {isExpanded && (
        <div className="mt-2 text-xs">
          <div className="font-medium text-gray-400 mb-1">Arguments:</div>
          <pre className="bg-black p-2 rounded mt-1 overflow-x-auto text-gray-400 border border-gray-800">
            {JSON.stringify(toolCall.arguments, null, 2)}
          </pre>

          <div className="font-medium mt-2 text-gray-400 mb-1">Result:</div>
          <pre className="bg-black p-2 rounded mt-1 overflow-x-auto text-gray-400 border border-gray-800">
            {JSON.stringify(toolCall.result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export { ToolCallDisplay };