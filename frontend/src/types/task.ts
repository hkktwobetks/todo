export type TaskStatus = "todo" | "in_progress" | "done";

export type Task = {
  id: number;
  title: string;
  status: TaskStatus;
  due_at: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
};

export type TaskPage = {
  items: Task[];
  total: number;
  limit: number;
  offset: number;
};

export type TaskCreate = {
  title: string;
  status: TaskStatus;
  due_at?: string | null;
};

export type TaskUpdate = {
  title?: string;
  status?: TaskStatus;
  due_at?: string | null;
};
