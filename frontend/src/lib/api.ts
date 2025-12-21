import { authClient } from "./auth-client";

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

      console.log("Better Auth session in ApiClient.getAuthHeaders:", session);

      // The session object from Better Auth should contain the session token
      // in session.session.token (what you showed in your JSON dump)
      if (session && session.session) {
        const token =
          session.session.token ||
          session.session.accessToken ||
          session.session.idToken ||
          session.session.id;

        if (token) {
          console.log(
            "Found session token, sending in Authorization header (Bearer ...)"
          );
          return { Authorization: `Bearer ${token}` };
        } else {
          console.warn(
            "No token-like value found on session.session. Full session:",
            session
          );
        }
      } else {
        console.warn(
          "No Better Auth session found when trying to build auth headers."
        );
      }
    } catch (error) {
      console.error("Failed to get auth session in ApiClient.getAuthHeaders:", error);
    }

    // If no session or no token found, return empty headers.
    // The backend will respond with 401 and the UI can handle it.
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

      // Some endpoints (like DELETE /tasks) return 204 No Content.
      // Calling response.json() on an empty body throws
      // "Unexpected end of JSON input", so we special-case it.
      if (response.status === 204) {
        return {
          success: true,
          data: undefined as T,
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
}

export const apiClient = new ApiClient();