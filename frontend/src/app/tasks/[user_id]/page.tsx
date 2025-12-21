"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { useAuth } from "@/lib/auth-client";
import { apiClient } from "@/lib/api";

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function TasksPage() {
  const { user_id } = useParams();
  const { user, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ title: "", description: "" });
  const [error, setError] = useState("");
  const [loadingTasks, setLoadingTasks] = useState(true);

  // Check if the current user matches the requested user_id
  useEffect(() => {
    if (authLoading) return; // Wait for auth to load first

    if (!user) {
      // User is not authenticated
      return;
    }

    if (user.id !== user_id) {
      setError("Access denied: You can only view your own tasks");
      return;
    }

    fetchTasks();
  }, [user, authLoading, user_id]);

  const fetchTasks = async () => {
    if (!user || user.id !== user_id) return;

    try {
      setLoadingTasks(true);
      const response = await apiClient.getTasks(user.id);

      if (response.success) {
        setTasks(response.data || []);
      } else {
        setError(response.error || "Failed to fetch tasks");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tasks");
    } finally {
      setLoadingTasks(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!user || user.id !== user_id) return;

    try {
      const response = await apiClient.createTask(user.id, {
        title: newTask.title,
        description: newTask.description,
      });

      if (response.success) {
        setTasks([...tasks, response.data]);
        setNewTask({ title: "", description: "" });
      } else {
        setError(response.error || "Failed to create task");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    }
  };

  const handleToggleTask = async (task: Task) => {
    if (!user || user.id !== user_id) return;

    try {
      const response = await apiClient.updateTask(user.id, task.id, {
        ...task,
        completed: !task.completed,
      });

      if (response.success) {
        setTasks(tasks.map(t =>
          t.id === task.id ? { ...t, completed: !t.completed } : t
        ));
      } else {
        setError(response.error || "Failed to update task");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user || user.id !== user_id) return;

    try {
      const response = await apiClient.deleteTask(user.id, taskId);

      if (response.success) {
        setTasks(tasks.filter(t => t.id !== taskId));
      } else {
        setError(response.error || "Failed to delete task");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task");
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h2>
          <p className="text-gray-600 mb-4">Please log in to view your tasks.</p>
          <a
            href="/login"
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Sign In
          </a>
        </div>
      </div>
    );
  }

  if (user.id !== user_id) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Access Denied</h2>
          <p className="text-gray-600 mb-2">{error}</p>
          <a
            href={`/tasks/${user.id}`}
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Go to Your Tasks
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Your Tasks</h1>

        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
            {error}
          </div>
        )}

        <form onSubmit={handleCreateTask} className="mb-8 p-4 bg-white rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Create New Task</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Task title"
              value={newTask.title}
              onChange={(e) => setNewTask({...newTask, title: e.target.value})}
              className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <input
              type="text"
              placeholder="Description"
              value={newTask.description}
              onChange={(e) => setNewTask({...newTask, description: e.target.value})}
              className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Add Task
          </button>
        </form>

        {loadingTasks ? (
          <div className="text-center py-8">Loading tasks...</div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <ul className="divide-y divide-gray-200">
              {tasks.length === 0 ? (
                <li className="p-4 text-center text-gray-500">No tasks found</li>
              ) : (
                tasks.map((task) => (
                  <li key={task.id} className="p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          checked={task.completed}
                          onChange={() => handleToggleTask(task)}
                          className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                        />
                        <span className={`ml-3 ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                          {task.title}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-500">
                          {new Date(task.created_at).toLocaleDateString()}
                        </span>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                    {task.description && (
                      <p className="ml-7 mt-1 text-sm text-gray-600">{task.description}</p>
                    )}
                  </li>
                ))
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}