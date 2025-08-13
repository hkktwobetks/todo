import { useState } from "react";
import type { TaskStatus } from "../types/task";
import { createTask } from "../api/tasks";
import { ApiError } from "../api/client";

export default function TaskForm({ onCreated }: { onCreated: () => void }) {
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState<TaskStatus>("todo");
  const [dueAt, setDueAt] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    setLoading(true);
    setErr(null);
    try {
      await createTask({
        title: title.trim(),
        status,
        due_at: dueAt ? new Date(dueAt).toISOString() : null,
      });
      setTitle("");
      setStatus("todo");
      setDueAt("");
      onCreated();
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : "failed to create");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={submit} style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="title"
        style={{ flex: "1 1 220px", padding: 8 }}
      />
      <select value={status} onChange={(e) => setStatus(e.target.value as TaskStatus)} style={{ padding: 8 }}>
        <option value="todo">todo</option>
        <option value="in_progress">in_progress</option>
        <option value="done">done</option>
      </select>
      <input
        type="datetime-local"
        value={dueAt}
        onChange={(e) => setDueAt(e.target.value)}
        style={{ padding: 8 }}
      />
      <button type="submit" disabled={loading} style={{ padding: "8px 12px" }}>
        {loading ? "…" : "Add"}
      </button>
      {err && <span style={{ color: "crimson", marginLeft: 8 }}>{err}</span>}
    </form>
  );
}
