import { useState } from "react";
import { Link } from "react-router-dom";
import type { Task, TaskStatus } from "../types/task";
import { deleteTask, toggleDone, updateTask } from "../api/tasks";
import { ApiError } from "../api/client";

export default function TaskItem({ task, onChanged }: { task: Task; onChanged: () => void }) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [status, setStatus] = useState<TaskStatus>(task.status);
  const [dueAt, setDueAt] = useState<string>(task.due_at ? toLocal(task.due_at) : "");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function save() {
    setLoading(true);
    setErr(null);
    try {
      await updateTask(task.id, {
        title: title.trim() || undefined,
        status,
        due_at: dueAt ? new Date(dueAt).toISOString() : null,
      });
      setEditing(false);
      onChanged();
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : "failed to update");
    } finally {
      setLoading(false);
    }
  }

  async function remove() {
    if (!confirm("Delete this task?")) return;
    setLoading(true);
    setErr(null);
    try {
      await deleteTask(task.id);
      onChanged();
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : "failed to delete");
    } finally {
      setLoading(false);
    }
  }

  async function toggle() {
    setLoading(true);
    setErr(null);
    try {
      await toggleDone(task);
      onChanged();
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : "failed to toggle");
    } finally {
      setLoading(false);
    }
  }

  return (
    <li style={{ padding: 12, border: "1px solid #e5e7eb", borderRadius: 8 }}>
      {editing ? (
        <div style={{ display: "grid", gap: 8 }}>
          <input value={title} onChange={(e) => setTitle(e.target.value)} />
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <select value={status} onChange={(e) => setStatus(e.target.value as TaskStatus)}>
              <option value="todo">todo</option>
              <option value="in_progress">in_progress</option>
              <option value="done">done</option>
            </select>
            <input type="datetime-local" value={dueAt} onChange={(e) => setDueAt(e.target.value)} />
            <button onClick={save} disabled={loading}>{loading ? "…" : "Save"}</button>
            <button onClick={() => setEditing(false)} disabled={loading}>Cancel</button>
          </div>
          {err && <div style={{ color: "crimson" }}>{err}</div>}
        </div>
      ) : (
        <div style={{ display: "grid", gap: 6 }}>
          <div style={{ fontWeight: 600 }}>
            <Link to={`/tasks/${task.id}`}>{task.title}</Link>
          </div>
          <div style={{ fontSize: 12, opacity: 0.7 }}>
            status: {task.status}
            {task.due_at ? ` · due: ${new Date(task.due_at).toLocaleString()}` : ""}
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => setEditing(true)} disabled={loading}>Edit</button>
            <button onClick={toggle} disabled={loading}>
              {task.status === "done" ? "Undo Done" : "Mark Done"}
            </button>
            <button onClick={remove} disabled={loading}>Delete</button>
          </div>
          {err && <div style={{ color: "crimson" }}>{err}</div>}
        </div>
      )}
    </li>
  );
}

function toLocal(iso: string) {
  // ISO文字列→input type="datetime-local" 用（タイムゾーンをローカルに合わせる簡易版）
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, "0");
  const yyyy = d.getFullYear();
  const mm = pad(d.getMonth() + 1);
  const dd = pad(d.getDate());
  const hh = pad(d.getHours());
  const mi = pad(d.getMinutes());
  return `${yyyy}-${mm}-${dd}T${hh}:${mi}`;
}
