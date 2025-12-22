import { betterAuth } from "better-auth";
import { db } from "./db-drizzle";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import * as schema from "../../drizzle/schema";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema: {
      user: schema.users,
      session: schema.sessions,
      account: schema.accounts,
      verification: schema.verifications,
    },
  }),
  secret: process.env.BETTER_AUTH_SECRET || "your-32-char-secret-here-make-it-secure",
  baseURL: process.env.BETTER_AUTH_URL || "https://todo-phase-ii.vercel.app",
  emailAndPassword: {
    enabled: true,
  },
  jwt: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
  },
  // Ensure session tokens are properly created and stored
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // Update session every 24 hours
  },
});