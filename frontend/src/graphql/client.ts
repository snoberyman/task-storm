import { GraphQLClient } from "graphql-request";

const url = import.meta.env.VITE_GRAPHQL_URL;
if (!url) {
  console.error("VITE_GRAPHQL_URL is not defined");
}

export const client = new GraphQLClient(url);
