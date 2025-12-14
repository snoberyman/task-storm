// src/lib/graphqlClient.ts
import { GraphQLClient } from "graphql-request";

export const client = new GraphQLClient(import.meta.env.VITE_GRAPHQL_URL, {
  headers: {
    // Add any auth headers if needed, e.g.,
    // Authorization: `Bearer ${token}`,
  },
});
