import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

// Export the auth API routes from Better Auth
const handler = toNextJsHandler(auth);
export const { GET, POST } = handler;