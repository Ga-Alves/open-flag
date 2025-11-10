import useFeatureFlags from "../../hooks/useFeatureFlags";
import FeatureFlagItem from "./FeatureFlagItem/FeatureFlagItem";

interface FeatureFlagListProps {
  onEdit: (flag: { id: number; name: string; description: string; status: boolean }) => void;
  onDelete: (flag: { id: number; name: string; description: string; status: boolean }) => void;
}

export default function FeatureFlagList({ onEdit, onDelete }: FeatureFlagListProps) {
  const { data, deleteFlag, toggleFlag } = useFeatureFlags();

  return (
    <ul className="flex flex-col gap-5 mt-5">
      {data.map((flag) => (
        <FeatureFlagItem
          key={flag.id}
          id={flag.id}
          name={flag.name}
          description={flag.description}
          status={flag.status}
          deleteFlag={deleteFlag}
          toogleFlag={toggleFlag}
          onEdit={() => onEdit(flag)}
          onDelete={() => onDelete(flag)}
        />
      ))}
    </ul>
  );
}
