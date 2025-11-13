import deleteIcon from "../../../assets/delete.svg";
import editIcon from "../../../assets/edit.svg";
import toggleOff from "../../../assets/toggle-off.svg";
import toggleOn from "../../../assets/toggle-on.svg";
import type { UpdateFlagRequest } from "../../../types/types";
import { DeleteFeatureFlagModal } from "../../Modal/DeleteFeatureFlagModal";
import { EditFeatureFlagModal } from "../../Modal/EditFeatureFlagModal";

type FeatureFlagItemProps = {
  name: string;
  description: string;
  value: boolean;
  deleteFlag: (name: string) => void;
  toggleFlag: (name: string) => void;
  updateFlag: (name: string, flagData: UpdateFlagRequest) => void;
};

export default function FeatureFlagItem(props: FeatureFlagItemProps) {
  const { name, description, value, deleteFlag, updateFlag, toggleFlag } = props;

  const onEdit = (flagData: UpdateFlagRequest) => updateFlag(name, flagData)

  return (
    <li className="flex items-center justify-between bg-gray-50 border rounded-lg p-4">
      <div className="w-1/2">
        <h2 className="text-lg font-bold text-blue-950">{name}</h2>
        <p className="text-black">{description}</p>
      </div>

      <div className="flex items-center justify-evenly w-1/2">
        <img
          src={value ? toggleOn : toggleOff}
          alt="toggle"
          className="cursor-pointer"
          onClick={() => toggleFlag(name)}
        />

        <EditFeatureFlagModal
          flag={{ name, description }}
          onConfirm={onEdit}
          trigger={
            <img
              src={editIcon}
              alt="edit"
              className="cursor-pointer"
            />
          }
        />

        <DeleteFeatureFlagModal
          onDelete={() => deleteFlag(name)}
          trigger={<img
            src={deleteIcon}
            alt="delete"
            className="cursor-pointer"
          />} />

      </div>
    </li>
  );
}
