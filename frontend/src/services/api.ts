import { Task } from '@/types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://todo-phase-ii.onrender.com';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      if (response.status === 204) {
        // No content for DELETE requests
        return { data: undefined as unknown as T };
      }

      const data = await response.json();

      // Handle date conversion for task objects
      if (endpoint === '/tasks' || endpoint.includes('/tasks/')) {
        if (Array.isArray(data)) {
          // Handle array of tasks (GET /tasks)
          return { data: this.convertTaskDates(data) as unknown as T };
        } else if (data && typeof data === 'object' && data.hasOwnProperty('id')) {
          // Handle single task (POST, PUT /tasks/{id})
          return { data: this.convertTaskDate(data) as unknown as T };
        }
      }

      return { data };
    } catch (error) {
      console.error('API request failed:', error);
      return { error: (error as Error).message || 'An error occurred' };
    }
  }

  private convertTaskDate(task: any): Task {
    return {
      ...task,
      createdAt: typeof task.createdAt === 'string' ? new Date(task.createdAt) : task.createdAt,
      updatedAt: typeof task.updatedAt === 'string' ? new Date(task.updatedAt) : task.updatedAt
    };
  }

  private convertTaskDates(tasks: any[]): Task[] {
    return tasks.map(task => this.convertTaskDate(task));
  }

  // Get all tasks
  async getTasks(): Promise<ApiResponse<Task[]>> {
    return this.request<Task[]>('/tasks');
  }

  // Create a new task
  async createTask(taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Promise<ApiResponse<Task>> {
    return this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  // Update a task
  async updateTask(id: string, taskData: Partial<Task>): Promise<ApiResponse<Task>> {
    // Prepare the update data, ensuring dates are in string format for the API
    const updateData = { ...taskData };

    // Remove id, createdAt, and updatedAt from update data since these shouldn't be updated
    delete updateData.id;
    delete updateData.createdAt;
    delete updateData.updatedAt;

    return this.request<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  // Delete a task
  async deleteTask(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string }>> {
    return this.request<{ status: string }>('/health');
  }
}

export const apiService = new ApiService(API_BASE_URL);

export default ApiService;