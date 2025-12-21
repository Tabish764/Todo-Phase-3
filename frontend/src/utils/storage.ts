import { Task } from '@/types/task';

const STORAGE_KEY = 'task-manager-data';

export interface PersistedData {
  tasks: Task[];
  lastUpdated: string;
}

export const loadTasksFromStorage = (): Task[] | null => {
  if (typeof window === 'undefined') return null;

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return null;

    const parsed: PersistedData = JSON.parse(stored);
    // Convert string dates back to Date objects
    return parsed.tasks?.map((task: any) => ({
      ...task,
      createdAt: new Date(task.createdAt),
      updatedAt: new Date(task.updatedAt)
    })) || null;
  } catch (error) {
    console.error('Error loading tasks from storage:', error);
    return null;
  }
};

export const saveTasksToStorage = (tasks: Task[]): void => {
  if (typeof window === 'undefined') return;

  try {
    const dataToStore: PersistedData = {
      tasks,
      lastUpdated: new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToStore));
  } catch (error) {
    console.error('Error saving tasks to storage:', error);
  }
};