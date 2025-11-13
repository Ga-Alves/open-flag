import useFeatureFlags from "../../hooks/useFeatureFlags";
import FeatureFlagItem from "./FeatureFlagItem/FeatureFlagItem";

export default function FeatureFlagList() {
  const { data } = useFeatureFlags();

  return (
    <ul className="flex flex-col gap-5 mt-5">
      {data.map((flag) => (
        <FeatureFlagItem
          key={flag.name}
          name={flag.name}
          description={flag.description}
          status={flag.status}
        />
      ))}
    </ul>
  );
}
