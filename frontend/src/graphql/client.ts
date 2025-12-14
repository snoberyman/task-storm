import { GraphQLClient } from "graphql-request";

// Adjust this to your backend URL
export const client = new GraphQLClient("http://localhost:8000/graphql");
