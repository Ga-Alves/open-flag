import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import FeatureFlagList from "./components/FeatureFlagList/FeatureFlagList";
import Header from "./components/Header/Header";

export default function App() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    navigate("/login");
  }

  return (
    <div className="min-h-dvh flex flex-col items-center transition-colors duration-300 bg-gray-50 dark:bg-[#0f172a]">
      <Header />

      <main className="w-11/12 md:w-2/3 lg:w-1/2 mt-12">

        {/* Barra com botões de ações */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-gray-100">
            Dashboard
          </h1>

          <div className="flex gap-3">
            <button
              onClick={() => navigate("/register")}
              className="px-4 py-2 rounded-md font-medium bg-blue-600 text-white hover:bg-blue-700 shadow-md transition"
            >
              Create User
            </button>

            <button
              onClick={logout}
              className="px-4 py-2 rounded-md font-medium bg-red-600 text-white hover:bg-red-700 shadow-md transition"
            >
              Logout
            </button>
          </div>
        </div>

        <FeatureFlagList />
      </main>
    </div>
  );
}
