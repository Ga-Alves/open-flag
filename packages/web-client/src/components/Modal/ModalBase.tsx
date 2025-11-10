import React from "react";

interface ModalBaseProps {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}

export const ModalBase: React.FC<ModalBaseProps> = ({ isOpen, title, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/50 z-50 flex justify-center items-center"
      onClick={onClose}
    >
      <div
        className="bg-[#f8fafc] rounded-xl shadow-lg w-full max-w-md p-6 relative"
        onClick={(e) => e.stopPropagation()} 
      >
        {/* botão de fechar */}
        <button
          onClick={onClose}
          className="absolute top-3 right-4 text-gray-500 hover:text-black text-lg"
          aria-label="Close modal"
        >
          ×
        </button>

        <h2 className="text-2xl font-semibold mb-4">{title}</h2>
        {children}
      </div>
    </div>
  );
};
