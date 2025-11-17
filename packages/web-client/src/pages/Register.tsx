import { useState } from "react";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail || "Registration failed");
      }

      setSuccess("User created successfully!");
      setName("");
      setEmail("");
      setPassword("");
      setConfirmPassword("");

    } catch (err: any) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-blue-800 dark:from-[#0f172a] dark:to-[#1e293b]">

      <div className="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-100 shadow-xl rounded-2xl w-full max-w-lg p-10">

        <h1 className="text-3xl font-extrabold text-blue-700 dark:text-blue-400 text-center mb-6">
          Create New User
        </h1>

        <form onSubmit={handleRegister} className="flex flex-col gap-5">

          <input
            type="text"
            placeholder="Full name"
            required
            className="px-3 py-2 bg-gray-50 dark:bg-gray-800 border rounded-md outline-none focus:ring-2 focus:ring-blue-500"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <input
            type="email"
            placeholder="email@example.com"
            required
            className="px-3 py-2 bg-gray-50 dark:bg-gray-800 border rounded-md outline-none focus:ring-2 focus:ring-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            required
            className="px-3 py-2 bg-gray-50 dark:bg-gray-800 border rounded-md outline-none focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <input
            type="password"
            placeholder="Confirm Password"
            required
            className="px-3 py-2 bg-gray-50 dark:bg-gray-800 border rounded-md outline-none focus:ring-2 focus:ring-blue-500"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />

          {error && <p className="text-red-500 text-center">{error}</p>}
          {success && <p className="text-green-500 text-center">{success}</p>}

          <button
            type="submit"
            className={`w-full py-2 rounded-md text-white font-medium transition ${
              loading
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Creating..." : "Create User"}
          </button>

        </form>
      </div>
    </div>
  );
}
