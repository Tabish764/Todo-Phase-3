import { NextRequest } from "next/server";
import { db } from "@/lib/db-drizzle";
import { jwks } from "../../../../drizzle/schema";

export async function GET(request: NextRequest) {
  try {
    // Fetch all JWKS keys from database
    const keys = await db.select().from(jwks);

    // Format as JWKS (JSON Web Key Set)
    const jwksResponse = {
      keys: keys.map((key) => {
        const publicKey = JSON.parse(key.publicKey);
        return {
          ...publicKey,
          kid: key.id, // Key ID
        };
      }),
    };

    // Return with caching headers
    return new Response(JSON.stringify(jwksResponse), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=3600", // Cache for 1 hour
      },
    });
  } catch (error) {
    console.error("Error in JWKS route:", error);
    return new Response(JSON.stringify({ error: "Internal server error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}