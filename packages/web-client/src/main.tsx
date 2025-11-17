import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function PublicOnlyRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem("token");

  if (token) {
    return <Navigate to="/" replace />;
  }

  return children;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <Routes>
      {/* Página inicial protegida */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <App />
          </ProtectedRoute>
        }
      />

      {/* Login só para usuário deslogado */}
      <Route
        path="/login"
        element={
          <PublicOnlyRoute>
            <Login />
          </PublicOnlyRoute>
        }
      />

      {/* Cadastro só para usuário logado (admin futuramente) */}
      <Route
        path="/register"
        element={
          <ProtectedRoute>
            <Register />
          </ProtectedRoute>
        }
      />

      {/* Rota inválida → redireciona */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  </BrowserRouter>
);
