import React, { useState, type ReactNode } from "react";
import { ModalBase } from "./ModalBase";

interface EditFeatureFlagModalProps {
  trigger: ReactNode;
  flag: { name: string; description: string };
  onConfirm: (data: { name: string; description: string }) => void;
}

export const EditFeatureFlagModal: React.FC<EditFeatureFlagModalProps> = ({
  flag,
  onConfirm,
  trigger
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [name, setName] = useState(flag.name);
  const [description, setDescription] = useState(flag.description);


  const onClose = () => setIsOpen(false)

  return (
    <>
      <div onClick={() => setIsOpen(curr => !curr)}>
        {trigger}
      </div>
      {
        isOpen &&

        <ModalBase isOpen={isOpen} title="Edit Feature Flag" onClose={onClose}>
          <div className="flex flex-col gap-4">
            <input
              className="border rounded-md p-2 bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <textarea
              className="border rounded-md p-2 bg-gray-50 min-h-[100px] focus:ring-2 focus:ring-blue-500 outline-none"
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
                onClick={() => onConfirm({ name, description })}
                className="px-4 py-2 rounded-md bg-green-600 hover:bg-green-700 text-white transition"
              >
                Save Changes
              </button>
            </div>
          </div>
        </ModalBase>
      }
    </>
  );
};
