const API_BASE = import.meta.env.VITE_API_BASE as string;

export class ApiError extends Error {
  status: number;
  payload: unknown;
  constructor(status: number, payload: unknown, message?: string) {
    super(message ?? `HTTP ${status}`);
    this.status = status;
    this.payload = payload;
  }
}

type FetchOptions = Omit<RequestInit, "body"> & { body?: unknown };

export async function apiFetch<T>(path: string, opts: FetchOptions = {}): Promise<T> {
  const url = `${API_BASE}${path}`;
  const headers = new Headers(opts.headers);
  if (!(opts.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  const res = await fetch(url, {
    ...opts,
    headers,
    body: opts.body ? (opts.body instanceof FormData ? opts.body : JSON.stringify(opts.body)) : undefined,
  });

  const ct = res.headers.get("Content-Type") ?? "";
  const isJson = ct.includes("application/json");
  const data = isJson ? await res.json().catch(() => undefined) : undefined;

  if (!res.ok) {
    const msg =
      (data && typeof (data as any).detail === "string" && (data as any).detail) ||
      (data && Array.isArray((data as any).detail) && JSON.stringify((data as any).detail)) ||
      `HTTP ${res.status}`;
    throw new ApiError(res.status, data, msg);
  }
  return (data as T) ?? (undefined as T);
}
