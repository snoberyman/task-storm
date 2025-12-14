interface TaskType {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: "LOW" | "MEDIUM" | "HIGH";
  tags: string[];
}

interface Props {
  task: TaskType;
  onToggle: (task: TaskType) => void;
  onDelete: (id: string) => void;
}

export default function TaskItem({ task, onToggle, onDelete }: Props) {
  // Background color based on priority
  const bgColor =
    task.priority === "HIGH"
      ? "bg-red-100"
      : task.priority === "MEDIUM"
      ? "bg-yellow-100"
      : "bg-green-100";

  return (
    <div
      className={`${bgColor} p-4 rounded shadow flex flex-col sm:flex-row sm:items-center sm:justify-between`}
    >
      <div>
        <h2
          className={`font-semibold ${
            task.completed ? "line-through text-gray-500" : ""
          }`}
        >
          {task.title}
        </h2>
        <p className="text-sm text-gray-600">{task.description}</p>

        {/* Tags */}
        {task.tags?.length > 0 && (
          <p className="text-xs mt-1 text-gray-700">
            Tags: {task.tags.join(", ")}
          </p>
        )}
      </div>

      <div className="space-x-2 mt-2 sm:mt-0">
        <button
          onClick={() => onToggle(task)}
          className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
        >
          {task.completed ? "Undo" : "Complete"}
        </button>

        <button
          onClick={() => onDelete(task.id)}
          className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
