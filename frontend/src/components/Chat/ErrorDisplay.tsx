import React from 'react';

interface ErrorDisplayProps {
  error: string;
  onRetry?: () => void;
}

const ErrorDisplay: React.FC<ErrorDisplayProps> = ({ error, onRetry }) => {
  // Determine error type based on message content
  const getErrorType = (errorMessage: string) => {
    if (errorMessage.includes('401') || errorMessage.toLowerCase().includes('unauthorized')) {
      return 'auth';
    } else if (errorMessage.includes('404')) {
      return 'not-found';
    } else if (errorMessage.includes('500') || errorMessage.toLowerCase().includes('server') || errorMessage.toLowerCase().includes('internal')) {
      return 'server';
    } else if (errorMessage.toLowerCase().includes('network') || errorMessage.toLowerCase().includes('fetch')) {
      return 'network';
    } else if (errorMessage.toLowerCase().includes('timeout')) {
      return 'timeout';
    } else {
      return 'general';
    }
  };

  const errorType = getErrorType(error);

  const getErrorMessage = () => {
    switch (errorType) {
      case 'auth':
        return 'Authentication failed. Please log in again.';
      case 'not-found':
        return 'The requested resource was not found.';
      case 'server':
        return 'Something went wrong on our end. Please try again.';
      case 'network':
        return 'Connection error. Check your internet and try again.';
      case 'timeout':
        return 'Request timed out. Please try again.';
      default:
        return error;
    }
  };

  const getErrorIcon = () => {
    switch (errorType) {
      case 'auth':
        return '🔒';
      case 'not-found':
        return '🔍';
      case 'server':
        return '⚙️';
      case 'network':
        return '🌐';
      case 'timeout':
        return '⏱️';
      default:
        return '⚠️';
    }
  };

  // Handle retry action
  const handleRetry = () => {
    if (errorType === 'auth') {
      // Redirect to login page
      window.location.href = '/login';
    } else if (onRetry) {
      onRetry();
    }
  };

  return (
    <div className="p-4 m-4 bg-gray-900 border border-gray-800 rounded-lg text-gray-300">
      <div className="flex items-start">
        <span className="mr-2 text-xl">{getErrorIcon()}</span>
        <div className="flex-1">
          <div className="font-semibold text-gray-200">Error</div>
          <div className="text-sm text-gray-400 mt-1">{getErrorMessage()}</div>
          {(onRetry || errorType === 'auth') && (
            <button
              onClick={handleRetry}
              className="mt-2 px-3 py-1 bg-gray-800 text-gray-100 text-xs rounded hover:bg-gray-700 transition-colors border border-gray-700"
            >
              {errorType === 'auth' ? 'Go to Login' : 'Retry'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export { ErrorDisplay };