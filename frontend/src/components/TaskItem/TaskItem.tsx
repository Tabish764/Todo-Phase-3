'use client';

import React, { useState, useEffect } from 'react';
import { Task } from '@/types/task';

interface TaskItemProps {
  task: Task;
  onToggleCompletion: (id: string) => Promise<void>;
  onEditTask: (id: string, title: string, description?: string) => Promise<void>;
  onDeleteTask: (id: string) => Promise<void>;
}

const TITLE_MIN_LENGTH = 1;
const TITLE_MAX_LENGTH = 200;
const DESCRIPTION_MAX_LENGTH = 1000;

const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onToggleCompletion,
  onEditTask,
  onDeleteTask
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isToggling, setIsToggling] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    if (!isEditing) setErrorMessage(null);
  }, [isEditing]);

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setErrors({});
    setErrorMessage(null);
  };

  const validateForm = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    if (!editTitle.trim()) {
      newErrors.title = 'Title is required';
    } else if (editTitle.length < TITLE_MIN_LENGTH || editTitle.length > TITLE_MAX_LENGTH) {
      newErrors.title = `Title must be between ${TITLE_MIN_LENGTH} and ${TITLE_MAX_LENGTH} characters`;
    }

    if (editDescription && editDescription.length > DESCRIPTION_MAX_LENGTH) {
      newErrors.description = `Description must not exceed ${DESCRIPTION_MAX_LENGTH} characters`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) return;

    setIsSaving(true);
    setErrorMessage(null);
    setIsEditing(false);

    // Fire-and-forget: operation updates state optimistically in the hook
    onEditTask(task.id, editTitle.trim(), editDescription.trim() || undefined)
      .catch((error) => {
        console.error('Failed to update task:', error);
        setErrorMessage('Error updating task. Try again.');
        setIsEditing(true);
      })
      .finally(() => {
        setIsSaving(false);
      });
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setErrors({});
    setErrorMessage(null);
  };

  const handleToggle = async () => {
    if (isToggling) return;
    setIsToggling(true);

    // Fire-and-forget: operation updates state optimistically in the hook
    onToggleCompletion(task.id)
      .catch((error) => {
        console.error('Failed to toggle completion:', error);
      })
      .finally(() => {
        setIsToggling(false);
      });
  };

  const handleDelete = async () => {
    if (window.confirm(`Delete task "${task.title}"?`)) {
      setIsDeleting(true);

      // Fire-and-forget: operation updates state optimistically in the hook
      onDeleteTask(task.id)
        .catch((error) => {
          console.error('Failed to delete task:', error);
        })
        .finally(() => {
          setIsDeleting(false);
        });
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') handleCancel();
    else if (e.key === 'Enter' && e.ctrlKey) handleSave();
  };

  if (isEditing) {
    return (
      <div 
        className="p-4 bg-gray-900 rounded-lg shadow-lg border border-gray-700 text-gray-100" 
        role="form" 
        aria-label={`Editing task: ${task.title}`}
        onKeyDown={handleKeyDown}
      >
        {errorMessage && (
          <div className="mb-3 p-3 bg-red-800 border border-red-600 rounded-md text-red-400" role="alert">
            {errorMessage}
          </div>
        )}
        <div className="mb-3">
          <label htmlFor={`edit-title-${task.id}`} className="block mb-1 font-medium">
            Title * <span className="text-sm text-gray-400">({editTitle.length}/{TITLE_MAX_LENGTH})</span>
          </label>
          <input
            id={`edit-title-${task.id}`}
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className={`w-full px-3 py-2 rounded-md focus:outline-none focus:ring-2 ${
              errors.title ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
            } bg-gray-800 text-gray-100`}
            aria-invalid={!!errors.title}
            aria-describedby={errors.title ? `edit-title-error-${task.id}` : undefined}
            maxLength={TITLE_MAX_LENGTH}
            disabled={isSaving}
            required
            autoFocus
          />
          {errors.title && <p id={`edit-title-error-${task.id}`} className="text-red-400 text-sm mt-1">{errors.title}</p>}
        </div>

        <div className="mb-3">
          <label htmlFor={`edit-description-${task.id}`} className="block mb-1 font-medium">
            Description <span className="text-sm text-gray-400">({editDescription.length}/{DESCRIPTION_MAX_LENGTH})</span>
          </label>
          <textarea
            id={`edit-description-${task.id}`}
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className={`w-full px-3 py-2 rounded-md focus:outline-none focus:ring-2 ${
              errors.description ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
            } bg-gray-800 text-gray-100`}
            rows={3}
            maxLength={DESCRIPTION_MAX_LENGTH}
            disabled={isSaving}
            aria-label="Edit task description"
            aria-invalid={!!errors.description}
            aria-describedby={errors.description ? `edit-description-error-${task.id}` : undefined}
          />
          {errors.description && <p id={`edit-description-error-${task.id}`} className="text-red-400 text-sm mt-1">{errors.description}</p>}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="Save task changes"
            >
              {isSaving ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancel}
              disabled={isSaving}
              className="px-4 py-2 bg-gray-700 text-white rounded-md hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="Cancel editing"
            >
              Cancel
            </button>
          </div>
          <p className="text-sm text-gray-400">
            Ctrl+Enter to save • Esc to cancel
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`p-4 bg-gray-900 rounded-lg shadow-lg transition-opacity ${
        task.completed ? 'opacity-60 line-through text-gray-500' : 'text-gray-100'
      } ${task.pending ? 'opacity-60 grayscale' : ''} ${isDeleting ? 'opacity-50' : ''}`}
    >
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          disabled={isToggling || isDeleting}
          className="mt-1 h-5 w-5 rounded border-gray-600 text-blue-500 focus:ring-blue-400 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
        />
        <div className="ml-3 flex-1">
          <div className="flex items-center">
            <h3 className={`text-lg font-medium ${task.pending ? 'italic' : ''}`}>
              {task.title}
            </h3>
            {task.pending && (
              <span className="ml-2 inline-flex items-center text-xs text-blue-400">
                <svg className="animate-spin -ml-1 mr-1 h-3 w-3 text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            )}
          </div>
          {task.description && <p className="mt-1 text-gray-400 whitespace-pre-wrap">{task.description}</p>}
          <div className="mt-2 text-sm text-gray-500">
            Created: {task.createdAt ? (typeof task.createdAt === 'string' ? new Date(task.createdAt).toLocaleDateString() : (task.createdAt as Date).toLocaleDateString()) : 'Unknown'} | Updated: {task.updatedAt ? (typeof task.updatedAt === 'string' ? new Date(task.updatedAt).toLocaleDateString() : (task.updatedAt as Date).toLocaleDateString()) : 'Unknown'}
          </div>
        </div>
        <div className="flex space-x-2" role="group" aria-label="Task actions">
          <button
            onClick={handleEdit}
            disabled={isDeleting}
            className="p-2 text-blue-400 hover:text-blue-500 rounded-full hover:bg-gray-800 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label={`Edit task: ${task.title}`}
          >
            ✏️
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="p-2 text-red-500 hover:text-red-600 rounded-full hover:bg-gray-800 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label={`Delete task: ${task.title}`}
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem;
