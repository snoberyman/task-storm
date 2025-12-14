import { gql } from "graphql-request";

export const GET_TASKS = gql`
  query {
    tasks {
      id
      title
      description
      completed
      priority
      tags
    }
  }
`;

export const CREATE_TASK = gql`
  mutation ($title: String!, $description: String) {
    createTask(title: $title, description: $description) {
      id
      title
      description
      completed
      priority
      tags
    }
  }
`;

export const UPDATE_TASK = gql`
  mutation (
    $id: ID!
    $title: String
    $description: String
    $completed: Boolean
  ) {
    updateTask(
      id: $id
      title: $title
      description: $description
      completed: $completed
    ) {
      id
      title
      description
      completed
      priority
      tags
    }
  }
`;

export const DELETE_TASK = gql`
  mutation ($id: ID!) {
    deleteTask(id: $id)
  }
`;

export const AUTO_PRIORITIZE_TASKS = gql`
  mutation {
    autoPrioritizeTasks {
      id
      title
      description
      completed
      priority
      tags
    }
  }
`;
