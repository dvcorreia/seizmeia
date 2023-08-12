import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Root from './routes/root'

const router = createBrowserRouter([
  { path: "/", element: <Root /> },
  { path: "/loggedin", element: <div>Logged in with cookie: {document.cookie}</div> },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
