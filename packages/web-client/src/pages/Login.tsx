import { useState } from "react";
import logo from "../assets/logo.svg"; // use o seu logo ou remova essa linha

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Simulação — substitua por sua lógica real de autenticação
    await new Promise((r) => setTimeout(r, 1000));

    if (email === "admin@openflag.dev" && password === "admin") {
      alert("Login successful!");
      // Redirecionar para a home (ex: usando react-router)
      window.location.href = "/";
    } else {
      setError("Invalid credentials");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-blue-800 dark:from-[#0f172a] dark:to-[#1e293b] transition-colors duration-300">
      <div className="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-100 shadow-2xl rounded-2xl w-full max-w-md p-10 animate-scaleIn">
        {/* Logo */}
        <div className="flex flex-col items-center mb-6">
          {logo && <img src={logo} alt="Open Flag Logo" className="w-16 mb-3" />}
          <h1 className="text-3xl font-extrabold text-blue-700 dark:text-blue-400">Open Flag</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Sign in to continue
          </p>
        </div>

        {/* Formulário */}
        <form onSubmit={handleLogin} className="flex flex-col gap-5">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="w-full border rounded-md px-3 py-2 bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="w-full border rounded-md px-3 py-2 bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          {error && (
            <p className="text-red-500 text-sm font-medium text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-2 rounded-md font-medium text-white transition-all shadow-md ${
              loading
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        {/* Rodapé */}
        <div className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>
            Forgot your password?{" "}
            <a href="#" className="text-blue-600 dark:text-blue-400 hover:underline">
              Reset it here
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
