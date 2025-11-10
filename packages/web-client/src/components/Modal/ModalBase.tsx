import React, { useEffect } from "react";

interface ModalBaseProps {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}

export const ModalBase: React.FC<ModalBaseProps> = ({
  isOpen,
  title,
  onClose,
  children,
}) => {
  // fecha com tecla ESC
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm animate-fadeIn"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 mx-4 transform transition-all animate-scaleIn"
      >
        {/* header */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-blue-900">{title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-800 transition"
            aria-label="Fechar modal"
          >
            ✕
          </button>
        </div>

        {/* conteúdo */}
        <div className="text-gray-800">{children}</div>
      </div>
    </div>
  );
};
