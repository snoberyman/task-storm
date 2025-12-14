import { GraphQLClient } from "graphql-request";

const url = import.meta.env.VITE_GRAPHQL_URL;
if (!url) {
  throw new Error(
    "VITE_GRAPHQL_URL is not defined. Check your .env file or Netlify env vars."
  );
}

export const client = new GraphQLClient(url);
