import { useEffect, useState } from "react";
import { client } from "./graphql/client";
import {
  GET_TASKS,
  CREATE_TASK,
  UPDATE_TASK,
  DELETE_TASK,
  AUTO_PRIORITIZE_TASKS,
} from "./graphql/queries";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";

export default function App() {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    const data = await client.request(GET_TASKS);
    setTasks(data.tasks);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const addTask = async (title: string, description: string) => {
    await client.request(CREATE_TASK, { title, description });
    // Auto-prioritize tasks after adding a new task
    try {
      const data = await client.request(AUTO_PRIORITIZE_TASKS);
      setTasks(data.autoPrioritizeTasks);
    } catch (err) {
      console.error("Failed to auto-prioritize tasks:", err);
      // Fallback to regular fetch if auto-prioritize fails
      fetchTasks();
    }
  };

  const toggleTask = async (task: {
    id: string;
    title: string;
    description: string;
    completed: boolean;
  }) => {
    await client.request(UPDATE_TASK, {
      id: task.id,
      completed: !task.completed,
    });
    fetchTasks();
  };

  const deleteTask = async (id: string) => {
    await client.request(DELETE_TASK, { id });
    fetchTasks();
  };

  return (
    <div className="max-w-xl mx-auto mt-10 font-sans">
      <h1 className="text-3xl font-bold mb-6 text-center">TaskStorm Demo</h1>
      <h4 className="text-xl font-semibold mb-0 text-center">
        AI-Powered Task Management
      </h4>
      <h3 className="text-lg mb-6 text-center text-gray-600">
        Organize and prioritize your tasks with ease!
      </h3>

      <TaskForm onAdd={addTask} />
      <TaskList tasks={tasks} onToggle={toggleTask} onDelete={deleteTask} />
    </div>
  );
}
