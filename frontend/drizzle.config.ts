import { defineConfig } from "drizzle-kit";

const DATABASE_URL = "postgresql://neondb_owner:npg_UNwVtq5m0HLo@ep-restless-salad-adv78p0z-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require";

export default defineConfig({
  dialect: "postgresql",
  schema: "./drizzle/schema.ts",
  dbCredentials: {
    url: DATABASE_URL,
  },
  out: "./drizzle/migrations",
  strict: true,
  verbose: true,
});
