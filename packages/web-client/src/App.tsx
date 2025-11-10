import { useState } from "react";
import add from "./assets/add-square.svg";
import Header from "./components/Header/Header";
import FeatureFlagList from "./components/FeatureFlagList/FeatureFlagList";
import { CreateFeatureFlagModal } from "./components/Modal/CreateFeatureFlagModal";
import { EditFeatureFlagModal } from "./components/Modal/EditFeatureFlagModal";
import { DeleteFeatureFlagModal } from "./components/Modal/DeleteFeatureFlagModal";

export default function App() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const [selectedFlag, setSelectedFlag] = useState<{
    id: number;
    name: string;
    description: string;
    status: boolean;
  } | null>(null);

  return (
    <div className="min-h-dvh flex flex-col items-center">
      <Header />
      <main className="w-1/2 mt-12">
        <div className="flex justify-between items-center">
          <h1 className="m-2 text-3xl font-bold text-blue-950">
            My Feature Flags
          </h1>

          {/* Botão para abrir modal de criação */}
          <img
            src={add}
            alt="add feature flag"
            className="cursor-pointer w-8 h-8 hover:scale-105 transition-transform"
            onClick={() => setIsCreateModalOpen(true)}
          />
        </div>

        <hr className="border-gray-200 mb-6" />

        <FeatureFlagList
          onEdit={(flag) => {
            setSelectedFlag(flag);
            setIsEditModalOpen(true);
          }}
          onDelete={(flag) => {
            setSelectedFlag(flag);
            setIsDeleteModalOpen(true);
          }}
        />

        {/* Modais */}
        <CreateFeatureFlagModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          onConfirm={(data) => {
            console.log("Nova flag criada:", data);
            setIsCreateModalOpen(false);
          }}
        />

        <EditFeatureFlagModal
          isOpen={isEditModalOpen}
          onClose={() => setIsEditModalOpen(false)}
          flag={
            selectedFlag
              ? {
                  name: selectedFlag.name,
                  description: selectedFlag.description,
                }
              : { name: "", description: "" }
          }
          onConfirm={(data) => {
            console.log("Flag editada:", data);
            setIsEditModalOpen(false);
          }}
        />

        <DeleteFeatureFlagModal
          isOpen={isDeleteModalOpen}
          onClose={() => setIsDeleteModalOpen(false)}
          onConfirm={() => {
            console.log("Flag excluída:", selectedFlag);
            setIsDeleteModalOpen(false);
          }}
        />
      </main>
    </div>
  );
}
