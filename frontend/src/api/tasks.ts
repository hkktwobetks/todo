import { apiFetch } from "./client";
import type { Task, TaskPage, TaskCreate, TaskUpdate, TaskStatus } from "../types/task";

function normalizeToPage(data: unknown, fallbackLimit = 10, fallbackOffset = 0): TaskPage {
  if (Array.isArray(data)) {
    const items = data as Task[];
    return { items, total: items.length, limit: fallbackLimit, offset: fallbackOffset };
  }
  const page = data as Partial<TaskPage> | undefined;
  return {
    items: page?.items ?? [],
    total: page?.total ?? (page?.items?.length ?? 0),
    limit: page?.limit ?? fallbackLimit,
    offset: page?.offset ?? fallbackOffset,
  };
}

// 一覧（フィルタ & ページング）: 返り値を必ずページ型に正規化
export async function listTasks(params?: {
  status?: TaskStatus;
  due_before?: string;
  limit?: number;
  offset?: number;
}): Promise<TaskPage> {
  const q = new URLSearchParams();
  if (params?.status) q.set("status", params.status);
  if (params?.due_before) q.set("due_before", params.due_before);
  if (params?.limit != null) q.set("limit", String(params.limit));
  if (params?.offset != null) q.set("offset", String(params.offset));
  const search = q.toString() ? `?${q.toString()}` : "";

  const raw = await apiFetch<unknown>(`/tasks/${search}`);
  return normalizeToPage(raw, params?.limit ?? 10, params?.offset ?? 0);
}

export function getTask(id: number) {
  return apiFetch<Task>(`/tasks/${id}`);
}

export function createTask(payload: TaskCreate) {
  return apiFetch<Task>("/tasks/", { method: "POST", body: payload });
}

export function updateTask(id: number, payload: TaskUpdate) {
  return apiFetch<Task>(`/tasks/${id}`, { method: "PUT", body: payload });
}

export function deleteTask(id: number) {
  return apiFetch<void>(`/tasks/${id}`, { method: "DELETE" });
}

export async function toggleDone(task: Task) {
  const next: TaskUpdate = { status: task.status === "done" ? "todo" : "done" };
  return updateTask(task.id, next);
}
