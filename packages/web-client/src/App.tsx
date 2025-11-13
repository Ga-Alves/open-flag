import FeatureFlagList from "./components/FeatureFlagList/FeatureFlagList";
import Header from "./components/Header/Header";

export default function App() {
  return (
    <div className="min-h-dvh flex flex-col items-center transition-colors duration-300 bg-gray-50 dark:bg-[#0f172a]">
      <Header />

      <main className="w-11/12 md:w-2/3 lg:w-1/2 mt-12">

        <FeatureFlagList />
      </main>
    </div>
  );
}
