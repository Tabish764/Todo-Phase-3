'use client';

import React from 'react';
import { Task } from '@/types/task';
import TaskItem from '../TaskItem/TaskItem';

interface TaskListProps {
  tasks: Task[];
  onToggleCompletion: (id: string) => Promise<void>;
  onEditTask: (id: string, title: string, description?: string) => Promise<void>;
  onDeleteTask: (id: string) => Promise<void>;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleCompletion,
  onEditTask,
  onDeleteTask
}) => {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-16 relative" role="status" aria-live="polite">
        <div className="relative inline-block">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-blue-600/20 blur-3xl"></div>
          <div className="relative">
            <svg className="w-24 h-24 mx-auto text-gray-700 mb-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <p className="text-gray-400 text-lg font-medium mb-2">No tasks yet</p>
            <p className="text-gray-600 text-sm">Create your first task to get started</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4" role="list" aria-label="List of tasks">
      {tasks.map((task, index) => (
        <div 
          key={task.id}
          className="animate-slide-up"
          style={{ animationDelay: `${index * 0.05}s` }}
        >
          <TaskItem
            task={task}
            onToggleCompletion={onToggleCompletion}
            onEditTask={onEditTask}
            onDeleteTask={onDeleteTask}
          />
        </div>
      ))}

      <style jsx>{`
        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-slide-up {
          animation: slide-up 0.4s ease-out forwards;
          opacity: 0;
        }
      `}</style>
    </div>
  );
};

export default TaskList;