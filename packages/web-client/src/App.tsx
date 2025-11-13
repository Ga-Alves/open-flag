import add from "./assets/add-square.svg";
import FeatureFlagList from "./components/FeatureFlagList/FeatureFlagList";
import Header from "./components/Header/Header";

export default function App() {
  return (
    <div className="min-h-dvh flex flex-col items-center transition-colors duration-300 bg-gray-50 dark:bg-[#0f172a]">
      <Header />

      <main className="w-11/12 md:w-2/3 lg:w-1/2 mt-12">
        <div className="flex justify-between items-center">
          <h1 className="m-2 text-4xl font-extrabold text-slate-900 dark:text-gray-100 tracking-tight drop-shadow-sm">
            My <span className="text-blue-600 dark:text-blue-400">Feature Flags</span>
          </h1>

          <button
            className="cursor-pointer w-9 h-9 flex items-center justify-center bg-white text-blue-700 font-bold rounded-md shadow-md hover:shadow-lg hover:scale-105 transition-all"
            aria-label="Add Feature Flag"
          >
            <img
              src={add}
              alt="add feature flag"
              className="w-6 h-6 invert dark:invert-0 opacity-90"
            />
          </button>
        </div>

        <hr className="border-gray-300 dark:border-gray-600 mb-6" />

        <FeatureFlagList />
      </main>
    </div>
  );
}
