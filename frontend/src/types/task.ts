export type TaskPriority = "low" | "medium" | "high";
export type TaskStatus = "pending" | "in_progress" | "completed";

export interface Category {
  id: string;
  name: string;
  user_id: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: TaskPriority;
  status: TaskStatus;
  deadline?: string;
  user_id: string;
  category_id?: string;
  created_at: string;
  category?: Category;
}
