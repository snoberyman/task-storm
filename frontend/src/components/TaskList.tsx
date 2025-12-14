import TaskItem from "./TaskItem";

interface TaskType {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: "LOW" | "MEDIUM" | "HIGH";
  tags: string[];
}

interface Props {
  tasks: TaskType[];
  onToggle: (task: TaskType) => void;
  onDelete: (id: string) => void;
}

export default function TaskList({
  tasks,
  onToggle,
  onDelete,
}: Props) {
  // Sort tasks by priority: HIGH -> MEDIUM -> LOW
  const sortedTasks = [...tasks].sort((a, b) => {
    const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  return (
    <div className="space-y-3">
      {sortedTasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
