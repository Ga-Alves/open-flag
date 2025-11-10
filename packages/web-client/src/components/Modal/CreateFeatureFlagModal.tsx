import React, { useState } from "react";
import { ModalBase } from "./ModalBase";

interface CreateFeatureFlagModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (data: { name: string; description: string }) => void;
}

export const CreateFeatureFlagModal: React.FC<CreateFeatureFlagModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
}) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  return (
    <ModalBase isOpen={isOpen} title="Create New Feature Flag" onClose={onClose}>
      <div className="flex flex-col gap-4">
        <input
          className="border rounded-md p-2 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none"
          placeholder="Flag name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <textarea
          className="border rounded-md p-2 bg-gray-50 min-h-[100px] focus:ring-2 focus:ring-blue-500 outline-none"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-md bg-gray-200 hover:bg-gray-300 text-gray-800 transition"
          >
            Cancel
          </button>
        <button
          onClick={() => {
            onConfirm({ name, description });
            setName("");
            setDescription("");
          }}
          className="px-5 py-2.5 rounded-lg font-medium text-white bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 shadow-md hover:shadow-lg transition-all"
        >
          Create Feature Flag
        </button>
        </div>
      </div>
    </ModalBase>
  );
};
