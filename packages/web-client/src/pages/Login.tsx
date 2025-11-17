import { useState } from "react";
import { api } from "../utils/api-client";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await api.login(email, password);

      localStorage.setItem("token", data.token);
      localStorage.setItem("email", email);

      window.location.href = "/";
    } catch (err: any) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-blue-800 dark:from-[#0f172a] dark:to-[#1e293b]">

      <div className="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-100 shadow-xl rounded-2xl w-full max-w-md p-10">

        <h1 className="text-3xl font-extrabold text-blue-700 dark:text-blue-400 text-center mb-6">
          Login
        </h1>

        <form onSubmit={handleLogin} className="flex flex-col gap-5">

          <input
            type="email"
            required
            placeholder="email@example.com"
            className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border rounded-md outline-none focus:ring-2 focus:ring-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            required
            placeholder="********"
            className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border rounded-md outline-none focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && (
            <p className="text-red-500 text-sm font-medium text-center">{error}</p>
          )}

          <button
            type="submit"
            className={`w-full py-2 rounded-md text-white font-medium transition ${
              loading
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>

        </form>
      </div>
    </div>
  );
}
