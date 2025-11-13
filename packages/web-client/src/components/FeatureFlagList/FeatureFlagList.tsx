import useFeatureFlags from "../../hooks/useFeatureFlags";
import FeatureFlagItem from "./FeatureFlagItem/FeatureFlagItem";

export default function FeatureFlagList() {
  const { data, deleteFlag, updateFlag } = useFeatureFlags();

  return (
    <ul className="flex flex-col gap-5 mt-5">
      {data.map((flag) => (
        <FeatureFlagItem
          key={flag.name}
          name={flag.name}
          description={flag.description}
          value={flag.value}
          deleteFlag={deleteFlag}
          updateFlag={updateFlag}
        />
      ))}
    </ul>
  );
}
