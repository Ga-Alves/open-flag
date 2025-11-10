import React, { useState } from "react";
import { ModalBase } from "./ModalBase";

interface EditFeatureFlagModalProps {
  isOpen: boolean;
  onClose: () => void;
  flag: { name: string; description: string };
  onConfirm: (data: { name: string; description: string }) => void;
}

export const EditFeatureFlagModal: React.FC<EditFeatureFlagModalProps> = ({
  isOpen,
  onClose,
  flag,
  onConfirm,
}) => {
  const [name, setName] = useState(flag.name);
  const [description, setDescription] = useState(flag.description);

  return (
    <ModalBase isOpen={isOpen} title="Edit Feature Flag" onClose={onClose}>
      <div className="flex flex-col gap-3">
        <label className="font-medium">Name</label>
        <input
          className="border rounded-md p-2 bg-gray-100"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <label className="font-medium">Description</label>
        <textarea
          className="border rounded-md p-2 bg-gray-100 min-h-[100px]"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <div className="flex justify-between mt-5">
          <button
            onClick={() => onConfirm({ name, description })}
            className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-md"
          >
            Confirm
          </button>
          <button
            onClick={onClose}
            className="bg-red-600 hover:bg-red-700 text-white px-5 py-2 rounded-md"
          >
            Close
          </button>
        </div>
      </div>
    </ModalBase>
  );
};
