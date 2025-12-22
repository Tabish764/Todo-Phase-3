import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL || "https://todo-phase-ii.vercel.app",
});

export const { signIn, signUp, signOut, useSession } = authClient;

export const useAuth = () => {
  const { data: session, isPending, error } = useSession();
  
  return {
    user: session?.user,
    session,
    loading: isPending,
    error,
    // Use explicit fetch calls for signup/signin so we can control payload and inspect responses
    login: async (email: string, password: string) => {
      try {
        const res = await fetch('/api/auth/sign-in/email', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          console.error('Auth sign-in error', res.status, data);
          return null;
        }
        // refresh client session (cookies are set by the endpoint)
        try {
          await authClient.getSession();
        } catch (e) {
          // non-fatal: session refresh failed but sign-in may still have succeeded
          console.warn('Failed to refresh session after sign-in', e);
        }
        return data;
      } catch (err) {
        console.error('Auth sign-in exception', err);
        return null;
      }
    },
    signup: async (email: string, password: string, name: string) => {
      try {
        const res = await fetch('/api/auth/sign-up/email', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name }),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          console.error('Auth sign-up error', res.status, data);
          return null;
        }
        // refresh client session so `useSession` sees the new session
        try {
          await authClient.getSession();
        } catch (e) {
          console.warn('Failed to refresh session after sign-up', e);
        }
        return data;
      } catch (err) {
        console.error('Auth sign-up exception', err);
        return null;
      }
    },
    logout: signOut,
  };
};