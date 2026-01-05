import { getCookie, setCookie } from 'cookies-next';
import { authClient } from './auth-client';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  private async getAuthHeaders(): Promise<Record<string, string>> {
    try {
      // Better Auth stores session information that includes session + user.
      // The client type is a union (data or error), so we cast to any here
      // because at runtime we know it has the `session` shape you logged.
      const raw = (await authClient.getSession()) as any;
      const session = raw?.data ?? raw;

      // The session object from Better Auth should contain the JWT token
      if (session && session.session) {
        // Better Auth typically stores the JWT token in different properties depending on the version
        // Common locations: session.session.token, session.session.accessToken, session.session.idToken
        // In many cases, the session.id IS the JWT token
        const token = session.session.token ||
                     session.session.accessToken ||
                     session.session.idToken ||
                     session.session.id;

        if (token) {
          console.log('Found token in session, sending in Authorization header');
          return { 'Authorization': `Bearer ${token}` };
        } else {
          console.warn('No token found in session. Session data:', session);
          // If no token found in session, we can still try with credentials
          // This allows cookies to be sent with the request
          console.warn('Sending request with credentials (cookies)');
          return {};
        }
      }
    } catch (error) {
      console.error('Failed to get auth session:', error);
    }

    // If no session or no token found, return empty headers
    // The backend will handle the authentication failure appropriately
    return {};
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const authHeaders = await this.getAuthHeaders();
    const headers = {
      'Content-Type': 'application/json',
      ...authHeaders,
      ...options.headers,
    };

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
        // Always include credentials for cross-origin requests to send cookies
        // This is essential for Better Auth session cookies to be sent
        credentials: 'include',
      });

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (parseError) {
          // If response is not JSON, use text
          const errorText = await response.text().catch(() => `HTTP error! status: ${response.status}`);
          return {
            success: false,
            error: errorText,
          };
        }

        return {
          success: false,
          error: errorData.detail || errorData.message || `HTTP error! status: ${response.status}`,
        };
      }

      const data = await response.json();
      return {
        success: true,
        data,
      };
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        return {
          success: false,
          error: 'Network error - please check your connection',
        };
      }

      return {
        success: false,
        error: error instanceof Error ? error.message : 'An unexpected error occurred',
      };
    }
  }

  // Task-related methods
  async getTasks(userId: string): Promise<ApiResponse<any[]>> {
    return this.request<any[]>(`/${userId}/tasks`);
  }

  async createTask(userId: string, taskData: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(userId: string, taskId: string, taskData: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(userId: string, taskId: string): Promise<ApiResponse<null>> {
    return this.request<null>(`/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  // Conversation-related methods
  async getConversations(userId: string, limit: number = 20, offset: number = 0): Promise<ApiResponse<any>> {
    return this.request<any>(`/${userId}/conversations?limit=${limit}&offset=${offset}`);
  }

  async getConversation(userId: string, conversationId: number): Promise<ApiResponse<any>> {
    return this.request<any>(`/${userId}/conversations/${conversationId}`);
  }

  async createConversation(userId: string, conversationData: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/${userId}/conversations`, {
      method: 'POST',
      body: JSON.stringify(conversationData),
    });
  }
}

export const apiClient = new ApiClient();