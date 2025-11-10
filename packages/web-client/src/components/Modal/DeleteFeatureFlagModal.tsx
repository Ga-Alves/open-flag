import React from "react";
import { ModalBase } from "./ModalBase";

interface DeleteFeatureFlagModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
}

export const DeleteFeatureFlagModal: React.FC<DeleteFeatureFlagModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
}) => {
  return (
    <ModalBase isOpen={isOpen} title="Delete Feature Flag" onClose={onClose}>
      <p className="text-gray-700 text-center mb-6">
        Are you sure you want to permanently delete this feature flag?
      </p>

      <div className="flex justify-center gap-4">
        <button
          onClick={onClose}
          className="px-4 py-2 rounded-md bg-gray-200 hover:bg-gray-300 text-gray-800 transition"
        >
          Cancel
        </button>
        <button
          onClick={onConfirm}
          className="px-4 py-2 rounded-md bg-red-600 hover:bg-red-700 text-white transition"
        >
          Delete
        </button>
      </div>
    </ModalBase>
  );
};
