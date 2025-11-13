import React, { useState, type ReactNode } from "react";
import { ModalBase } from "./ModalBase";

interface DeleteFeatureFlagModalProps {
  trigger: ReactNode;
  onDelete: () => void;
}

export const DeleteFeatureFlagModal: React.FC<DeleteFeatureFlagModalProps> = ({
  trigger,
  onDelete,
}) => {

  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <div onClick={() => setIsOpen((currState) => !currState)}>
        {trigger}
      </div>

      {
        isOpen &&

        <ModalBase isOpen={isOpen} title="Delete Feature Flag" onClose={() => setIsOpen(false)}>
          <p className="text-gray-700 text-center mb-6">
            Are you sure you want to permanently delete this feature flag?
          </p>

          <div className="flex justify-center gap-4">
            <button
              onClick={() => setIsOpen(false)}
              className="px-4 py-2 rounded-md bg-gray-200 hover:bg-gray-300 text-gray-800 transition"
            >
              Cancel
            </button>
            <button
              onClick={onDelete}
              className="px-4 py-2 rounded-md bg-red-600 hover:bg-red-700 text-white transition"
            >
              Delete
            </button>
          </div>
        </ModalBase>
      }
    </>
  );
};
