import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "../../drizzle/schema";

// Create a connection with proper async configuration
const client = postgres(process.env.DATABASE_URL || "postgresql://localhost/taskdb", {
  max: 1,
  idle_timeout: 30,
});

// Create the database connection
export const db = drizzle(client, { schema });