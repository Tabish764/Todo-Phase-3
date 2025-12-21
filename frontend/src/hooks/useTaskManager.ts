import { useState, useEffect } from 'react';
import { Task } from '@/types/task';
import { apiClient } from '@/lib/api';
import { useAuth } from '@/lib/auth-client';

// Helper function to generate temporary IDs for optimistic updates
const generateTempId = (): string => {
  return `temp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

export const useTaskManager = () => {
  const { user, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);

  // Load tasks from API on mount
  useEffect(() => {
    // Wait until auth state is resolved
    if (authLoading) return;

    // No logged-in user: stop loading and show auth message
    if (!user) {
      setLoading(false);
      setError("Please log in to view tasks");
      setHasLoadedOnce(false);
      return;
    }

    // Avoid refetching tasks on every small authClient revalidation:
    // only fetch once per user.id (or after logout/login).
    if (hasLoadedOnce) return;

    const fetchTasks = async () => {
      setLoading(true);
      setError(null);
      const response = await apiClient.getTasks(user.id);

      if (response.error) {
        setError(response.error);
        console.error("Failed to fetch tasks:", response.error);
      } else if (response.data) {
        setTasks(response.data);
      }

      setLoading(false);
      setHasLoadedOnce(true);
    };

    fetchTasks();
  }, [user?.id, authLoading, hasLoadedOnce]);

  const createTask = async (title: string, description?: string): Promise<Task | null> => {
    if (!user) {
      setError('Please log in to create tasks');
      return null;
    }

    // Generate temporary ID and create optimistic task
    const tempId = generateTempId();
    const optimisticTask: Task = {
      id: tempId,
      title,
      description,
      completed: false,
      createdAt: new Date(),
      updatedAt: new Date(),
      pending: true,
      tempId
    };

    // Add optimistic task to UI immediately
    setTasks(prev => [...prev, optimisticTask]);

    try {
      const response = await apiClient.createTask(user.id, { title, description, completed: false });

      if (response.error) {
        console.error('Failed to create task:', response.error);
        // Remove the optimistic task from UI on failure
        setTasks(prev => prev.filter(task => task.id !== tempId));
        setError(response.error);
        return null;
      }

      if (response.data) {
        // Update the optimistic task with real server data
        setTasks(prev =>
          prev.map(task =>
            task.id === tempId
              ? { ...response.data!, pending: false, tempId: undefined } // Clear pending and tempId
              : task
          )
        );
        setError(null); // Clear any previous errors
        return response.data;
      }

      // If no response data, remove the optimistic task
      setTasks(prev => prev.filter(task => task.id !== tempId));
      return null;
    } catch (error) {
      // Remove the optimistic task from UI on exception
      setTasks(prev => prev.filter(task => task.id !== tempId));
      setError('An unexpected error occurred while creating the task');
      console.error('Unexpected error in createTask:', error);
      return null;
    }
  };

  const updateTask = async (id: string, updates: Partial<Task>): Promise<Task | null> => {
    if (!user) {
      setError('Please log in to update tasks');
      return null;
    }

    // Find the current task for potential reversion
    const currentTask = tasks.find(task => task.id === id);
    if (!currentTask) {
      const errorMsg = `Task with id ${id} not found for update`;
      console.error(errorMsg);
      setError(errorMsg);
      return null;
    }

    // Store original state for potential reversion
    const originalTask = { ...currentTask };

    // Optimistic update: apply changes immediately to UI
    const optimisticTask = { ...currentTask, ...updates };
    setTasks(prev =>
      prev.map(task => (task.id === id ? optimisticTask : task))
    );

    try {
      const response = await apiClient.updateTask(user.id, id, updates);

      if (response.error) {
        console.error('Failed to update task:', response.error);
        // Revert to original state on failure
        setTasks(prev =>
          prev.map(task => (task.id === id ? originalTask : task))
        );
        setError(response.error);
        return null;
      }

      if (response.data) {
        // Update with server response (in case server modified data)
        setTasks(prev =>
          prev.map(task => (task.id === id ? response.data! : task))
        );
        setError(null); // Clear any previous errors
        return response.data;
      }

      // No response data, revert to original
      setTasks(prev =>
        prev.map(task => (task.id === id ? originalTask : task))
      );
      setError('Failed to update task: No response data');
      return null;
    } catch (error) {
      // Revert to original state on exception
      setTasks(prev =>
        prev.map(task => (task.id === id ? originalTask : task))
      );
      setError('An unexpected error occurred while updating the task');
      console.error('Unexpected error in updateTask:', error);
      return null;
    }
  };

  const deleteTask = async (id: string): Promise<void> => {
    if (!user) {
      setError('Please log in to delete tasks');
      throw new Error('Please log in to delete tasks');
    }

    // Find the task to be deleted for potential restoration
    const taskToDelete = tasks.find(task => task.id === id);

    if (!taskToDelete) {
      const errorMsg = `Task with id ${id} not found for deletion`;
      console.error(errorMsg);
      setError(errorMsg);
      throw new Error(errorMsg);
    }

    // Optimistically remove the task from UI
    setTasks(prev => prev.filter(task => task.id !== id));

    try {
      const response = await apiClient.deleteTask(user.id, id);

      if (response.error) {
        console.error('Failed to delete task:', response.error);
        // Add the task back to the UI on failure
        setTasks(prev => [...prev, taskToDelete]);
        setError(response.error);
        throw new Error(response.error);
      }

      setError(null); // Clear any previous errors
    } catch (error) {
      // Add the task back to the UI on exception
      setTasks(prev => [...prev, taskToDelete]);
      setError('An unexpected error occurred while deleting the task');
      console.error('Unexpected error in deleteTask:', error);
      throw error;
    }
  };

  const toggleTaskCompletion = async (id: string): Promise<void> => {
    if (!user) {
      setError('Please log in to update tasks');
      throw new Error('Please log in to update tasks');
    }

    const currentTask = tasks.find(t => t.id === id);
    if (!currentTask) {
      const errorMsg = `Task with id ${id} not found for toggle completion`;
      console.error(errorMsg);
      setError(errorMsg);
      throw new Error(errorMsg);
    }

    // Store original state for potential reversion
    const originalCompleted = currentTask.completed;

    // Optimistic update
    setTasks(prev =>
      prev.map(task =>
        task.id === id ? { ...task, completed: !originalCompleted } : task
      )
    );

    try {
      const result = await updateTask(id, { completed: !originalCompleted });

      // If update failed, revert the optimistic update
      if (!result) {
        setTasks(prev =>
          prev.map(task =>
            task.id === id ? { ...task, completed: originalCompleted } : task
          )
        );
        setError('Failed to update task completion status');
      } else {
        setError(null); // Clear any previous errors
      }
    } catch (error) {
      // Revert the optimistic update on exception
      setTasks(prev =>
        prev.map(task =>
          task.id === id ? { ...task, completed: originalCompleted } : task
        )
      );
      setError('An unexpected error occurred while updating task completion');
      console.error('Unexpected error in toggleTaskCompletion:', error);
    }
  };

  return {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion
  };
};