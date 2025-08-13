import { useEffect, useMemo, useState } from "react";
import TaskForm from "../components/TaskForm";
import TaskItem from "../components/TaskItem";
import { listTasks } from "../api/tasks";
import type { Task, TaskStatus, TaskPage } from "../types/task";
import { ApiError } from "../api/client";

export default function TaskList() {
  const [items, setItems] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [limit, setLimit] = useState(10);
  const [offset, setOffset] = useState(0);

  const [status, setStatus] = useState<TaskStatus | "">("");
  const [dueBefore, setDueBefore] = useState<string>("");

  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  const page = useMemo(() => Math.floor(offset / limit) + 1, [offset, limit]);
  const pages = useMemo(() => Math.max(1, Math.ceil(total / limit)), [total, limit]);

  async function reload() {
    setLoading(true);
    setErr(null);
    try {
      const pageData = await listTasks({
        status: (status || undefined) as TaskStatus | undefined,
        due_before: dueBefore ? new Date(dueBefore).toISOString() : undefined,
        limit,
        offset,
      });
      setItems(pageData.items);
      setTotal(pageData.total);
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : "failed to fetch");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [limit, offset, status, dueBefore]);

  return (
    <div>
      <TaskForm onCreated={() => { setOffset(0); reload(); }} />

      {/* フィルタ */}
      <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 12, flexWrap: "wrap" }}>
        <select value={status} onChange={(e) => { setOffset(0); setStatus(e.target.value as any); }}>
          <option value="">(all)</option>
          <option value="todo">todo</option>
          <option value="in_progress">in_progress</option>
          <option value="done">done</option>
        </select>
        <input
          type="date"
          value={dueBefore}
          onChange={(e) => { setOffset(0); setDueBefore(e.target.value); }}
        />
        <span style={{ opacity: 0.7 }}>total: {total}</span>
      </div>

      {/* 一覧 */}
      {loading ? (
        <div>loading...</div>
      ) : err ? (
        <div style={{ color: "crimson" }}>{err}</div>
      ) : (
        <ul style={{ display: "grid", gap: 8, padding: 0, listStyle: "none" }}>
          {(items ?? []).map((t) => (
            <TaskItem key={t.id} task={t} onChanged={reload} />
          ))}
        </ul>
      )}

      {/* ページネーション */}
      <div style={{ display: "flex", gap: 8, alignItems: "center", marginTop: 16 }}>
        <button disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - limit))}>
          Prev
        </button>
        <span>Page {page} / {pages}</span>
        <button disabled={offset + limit >= total} onClick={() => setOffset(offset + limit)}>
          Next
        </button>
        <select value={limit} onChange={(e) => { setOffset(0); setLimit(Number(e.target.value)); }}>
          {[5, 10, 20, 50].map(n => <option key={n} value={n}>{n}/page</option>)}
        </select>
      </div>
    </div>
  );
}
