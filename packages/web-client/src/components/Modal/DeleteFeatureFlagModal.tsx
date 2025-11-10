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
      <p className="text-gray-700 mb-6">
        Do you really want to delete this feature flag?<br />
        <span className="text-red-600 font-semibold">
          This action can’t be undone.
        </span>
      </p>
      <div className="flex justify-between">
        <button
          onClick={onConfirm}
          className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-md"
        >
          Confirm
        </button>
        <button
          onClick={onClose}
          className="bg-yellow-500 hover:bg-yellow-600 text-white px-5 py-2 rounded-md"
        >
          Cancel
        </button>
      </div>
    </ModalBase>
  );
};
