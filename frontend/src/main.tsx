import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import TaskList from "./pages/TaskList";
import TaskDetail from "./pages/TaskDetail";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <TaskList /> },            // / → 一覧
      { path: "tasks/:taskId", element: <TaskDetail /> } // /tasks/1 → 詳細
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
