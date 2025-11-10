import deleteIcon from "../../../assets/delete.svg";
import editIcon from "../../../assets/edit.svg";
import toggleOff from "../../../assets/toggle-off.svg";
import toggleOn from "../../../assets/toggle-on.svg";

type FeatureFlagItemProps = {
  id: number;
  name: string;
  description: string;
  status: boolean;
  deleteFlag: (id: number) => void;
  toogleFlag: (id: number, currentStatus: boolean) => void;
  onEdit: () => void;
  onDelete: () => void;
};

export default function FeatureFlagItem(props: FeatureFlagItemProps) {
  const { id, name, description, status, deleteFlag, toogleFlag, onEdit, onDelete } = props;

  return (
    <li className="flex items-center justify-between bg-gray-50 border rounded-lg p-4">
      <div className="w-1/2">
        <h2 className="text-lg font-bold text-blue-950">{name}</h2>
        <p>{description}</p>
      </div>

      <div className="flex items-center justify-evenly w-1/2">
        <img
          src={status ? toggleOn : toggleOff}
          alt="toggle"
          className="cursor-pointer"
          onClick={() => toogleFlag(id, status)}
        />

        {/* Agora chama o modal real de edição */}
        <img
          src={editIcon}
          alt="edit"
          className="cursor-pointer"
          onClick={onEdit}
        />

        {/* Agora chama o modal real de exclusão */}
        <img
          src={deleteIcon}
          alt="delete"
          className="cursor-pointer"
          onClick={onDelete}
        />
      </div>
    </li>
  );
}
