import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getTask } from "../api/tasks";
import type { Task } from "../types/task";
import { ApiError } from "../api/client";

export default function TaskDetail() {
  const { taskId } = useParams();
  const id = Number(taskId);
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      if (!id) return;
      setLoading(true);
      setErr(null);
      try {
        const t = await getTask(id);
        setTask(t);
      } catch (e) {
        setErr(e instanceof ApiError ? e.message : "failed to fetch");
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (!id) return <div>Invalid id</div>;
  if (loading) return <div>loading...</div>;
  if (err) return <div style={{ color: "crimson" }}>{err}</div>;
  if (!task) return <div>Not found</div>;

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <Link to="..">← Back</Link>
      </div>
      <h2 style={{ marginTop: 0 }}>{task.title}</h2>
      <div>Status: {task.status}</div>
      <div>Due: {task.due_at ? new Date(task.due_at).toLocaleString() : "-"}</div>
      <div>Created: {new Date(task.created_at).toLocaleString()}</div>
      <div>Updated: {new Date(task.updated_at).toLocaleString()}</div>
      {task.completed_at && <div>Completed: {new Date(task.completed_at).toLocaleString()}</div>}
    </div>
  );
}
