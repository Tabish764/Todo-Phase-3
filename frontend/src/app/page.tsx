'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import TaskForm from '@/components/TaskForm/TaskForm';
import TaskList from '@/components/TaskList/TaskList';
import { useTaskManager } from '@/hooks/useTaskManager';
import { useAuth } from '@/lib/auth-client';

export default function Home() {
  const { user, loading: authLoading, logout } = useAuth();
  const {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion
  } = useTaskManager();

  const [notification, setNotification] = useState<{
    message: string;
    type: 'success' | 'error';
  } | null>(null);

  const showNotification = (message: string, type: 'success' | 'error') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  // Wrapper function to match TaskList's expected signature
  const handleEditTask = async (id: string, title: string, description?: string): Promise<void> => {
    showNotification('Task updated successfully', 'success');
    updateTask(id, { title, description }).catch(() => {
      showNotification('Failed to update task', 'error');
    });
  };

  // Wrapper function for task creation
  const handleCreateTask = async (title: string, description?: string): Promise<void> => {
    showNotification('Task created successfully', 'success');
    createTask(title, description).catch(() => {
      showNotification('Failed to create task', 'error');
    });
  };

  const handleDeleteTask = async (id: string): Promise<void> => {
    showNotification('Task deleted successfully', 'success');
    deleteTask(id).catch(() => {
      showNotification('Failed to delete task', 'error');
    });
  };

  if (loading || authLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="relative">
          <div className="w-20 h-20 border-4 border-gray-800 border-t-purple-500 rounded-full animate-spin"></div>
          <p className="text-gray-400 mt-4 text-center">Loading tasks...</p>
        </div>
      </div>
    );
  }

  // If not authenticated, show login/signup buttons
  if (!user) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="relative">
          <div className="fixed inset-0 overflow-hidden pointer-events-none">
            <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-purple-900/20 via-transparent to-transparent blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-blue-900/20 via-transparent to-transparent blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
          </div>

          <div className="relative z-10 text-center">
            <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent animate-gradient mb-4">
              Task Manager
            </h1>
            <p className="text-gray-400 text-lg mb-12">Organize your life in style</p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/signup"
                className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-lg hover:opacity-90 transition-opacity backdrop-blur-xl"
              >
                Sign Up
              </Link>
              <Link
                href="/login"
                className="px-8 py-3 bg-gray-700 text-white font-semibold rounded-lg hover:bg-gray-600 transition-colors backdrop-blur-xl border border-gray-600"
              >
                Login
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Animated background gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-purple-900/20 via-transparent to-transparent blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-blue-900/20 via-transparent to-transparent blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Notification Toast */}
      {notification && (
        <div className="fixed top-6 right-6 z-50 animate-slide-in">
          <div className={`px-6 py-4 rounded-lg shadow-2xl backdrop-blur-xl border ${
            notification.type === 'success' 
              ? 'bg-green-500/10 border-green-500/50 text-green-400' 
              : 'bg-red-500/10 border-red-500/50 text-red-400'
          }`}>
            <div className="flex items-center space-x-3">
              {notification.type === 'success' ? (
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
              <p className="font-medium">{notification.message}</p>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-5xl mx-auto px-4 py-12 relative z-10">
        <header className="mb-12">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent animate-gradient">
                Task Manager
              </h1>
              <p className="text-gray-400 text-lg mt-2">Organize your life in style</p>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-gray-300 text-sm">
                {user?.email}
              </span>
              <button
                onClick={async () => {
                  await logout();
                  window.location.reload();
                }}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 text-red-400 rounded-xl backdrop-blur-xl" role="alert">
            <div className="flex items-center space-x-3">
              <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p>{error}</p>
            </div>
          </div>
        )}

        <main role="main">
          <TaskForm onCreateTask={handleCreateTask} />

          <div className="mb-6 flex justify-between items-center px-1">
            <h2 className="text-2xl font-semibold text-gray-200" id="tasks-heading">Your Tasks</h2>
            <span className="px-4 py-1 bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-500/30 rounded-full text-gray-300 text-sm font-medium backdrop-blur-xl">
              {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
            </span>
          </div>

          <TaskList
            tasks={tasks}
            onToggleCompletion={toggleTaskCompletion}
            onEditTask={handleEditTask}
            onDeleteTask={handleDeleteTask}
          />
        </main>

        <footer className="mt-16 text-center text-gray-600 text-sm" role="contentinfo">
          <p>✨ All tasks are securely stored on the backend server</p>
        </footer>
      </div>

      <style jsx>{`
        @keyframes slide-in {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        @keyframes gradient {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }
        .animate-slide-in {
          animation: slide-in 0.3s ease-out;
        }
        .animate-gradient {
          background-size: 200% auto;
          animation: gradient 3s ease infinite;
        }
      `}</style>
    </div>
  );
}