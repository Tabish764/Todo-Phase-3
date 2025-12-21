'use client';

import React, { useState } from 'react';
import { Task } from '@/types/task';

interface TaskFormProps {
  onCreateTask: (title: string, description?: string) => Promise<void>;
}

const TaskForm: React.FC<TaskFormProps> = ({ onCreateTask }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState<{ title?: string }>({});

  const validateForm = (): boolean => {
    const newErrors: { title?: string } = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.length < 1 || title.length > 200) {
      newErrors.title = 'Title must be between 1 and 200 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      const taskTitle = title;
      const taskDescription = description;
      
      // Clear form immediately (fire-and-forget)
      setTitle('');
      setDescription('');
      setErrors({});

      // Fire the operation without awaiting
      onCreateTask(taskTitle, taskDescription).catch((error) => {
        console.error('Failed to create task:', error);
        // Restore form on failure
        setTitle(taskTitle);
        setDescription(taskDescription);
      });
    }
  };

  return (
    <form 
      onSubmit={handleSubmit} 
      className="mb-6 p-4 bg-gray-900 rounded-lg shadow-lg border border-gray-700 text-gray-100"
      role="form"
      aria-label="Task creation form"
    >
      <div className="mb-4">
        <label htmlFor="title" className="block mb-2 font-medium">
          Task Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className={`w-full px-3 py-2 rounded-md focus:outline-none focus:ring-2 ${
            errors.title ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
          } bg-gray-800 text-gray-100`}
          placeholder="Enter task title (1-200 characters)"
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? "title-error" : undefined}
          required
          autoFocus
        />
        {errors.title && <p id="title-error" className="text-red-400 text-sm mt-1">{errors.title}</p>}
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="block mb-2 font-medium">
          Description (Optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-800 text-gray-100 border border-gray-600"
          placeholder="Enter task description"
          rows={3}
          aria-label="Task description"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-2 px-4 rounded-md transition duration-200"
        aria-label="Add new task"
      >
        Add Task
      </button>
    </form>
  );
};

export default TaskForm;
