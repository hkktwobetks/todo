import { Link, Outlet } from "react-router-dom";

export default function App() {
  return (
    <div style={{ maxWidth: 800, margin: "32px auto", padding: 16 }}>
      <header style={{ display: "flex", gap: 16, alignItems: "center" }}>
        <h1 style={{ margin: 0 }}>Todo</h1>
        <nav style={{ display: "flex", gap: 12 }}>
          <Link to="/">Tasks</Link>
        </nav>
      </header>
      <main style={{ marginTop: 24 }}>
        <Outlet />
      </main>
    </div>
  );
}
