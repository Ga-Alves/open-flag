import useFeatureFlags from "../../hooks/useFeatureFlags";
import { CreateFeatureFlagModal } from "../Modal/CreateFeatureFlagModal";
import FeatureFlagItem from "./FeatureFlagItem/FeatureFlagItem";
import add from "../../assets/add-square.svg";


export default function FeatureFlagList() {
  const { data, deleteFlag, updateFlag, toggleFlag, createFlag } = useFeatureFlags();

  return (
    <>
      <div className="flex justify-between items-center">
        <h1 className="m-2 text-4xl font-extrabold text-slate-900 dark:text-gray-100 tracking-tight drop-shadow-sm">
          My <span className="text-blue-600 dark:text-blue-400">Feature Flags</span>
        </h1>

        <CreateFeatureFlagModal
          onConfirm={createFlag}
          trigger={
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
          }
        />
      </div>

      <hr className="border-gray-300 dark:border-gray-600 mb-6" />
      <ul className="flex flex-col gap-5 mt-5">
        {data.map((flag) => (
          <FeatureFlagItem
            key={flag.name}
            name={flag.name}
            description={flag.description}
            value={flag.value}
            deleteFlag={deleteFlag}
            updateFlag={updateFlag}
            toggleFlag={toggleFlag}
          />
        ))}
      </ul>
    </>
  );
}
