import useFeatureFlags from "../../hooks/useFeatureFlags";
import FeatureFlagItem from "./FeatureFlagItem/FeatureFlagItem";


export default function FeatureFlagList() {
    const {data, deleteFlag, toggleFlag} = useFeatureFlags();

    return (
        <ul className=" flex flex-col gap-5 mt-5">
            {data.map(flag =>
                <FeatureFlagItem
                    key={flag.id}
                    id={flag.id}
                    name={flag.name}
                    description={flag.description}
                    status={flag.status}
                    deleteFlag={deleteFlag}
                    toogleFlag={toggleFlag} />
            )}
        </ul>
    )
}