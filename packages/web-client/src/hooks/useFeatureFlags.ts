import { useState, useEffect } from "react";
import { FeatureFlagClient } from "../utils/api-client";
import type {
  FeatureFlag,
  CreateFlagRequest,
  UpdateFlagRequest,
} from "../types/types";

export default function useFeatureFlags() {
  const [flags, setFlags] = useState<FeatureFlag[]>([]);

  const client = new FeatureFlagClient();

  useEffect(() => {
    loadFlags();
  }, []);

  const loadFlags = async () => {
    const data = await client.listAllFlags();
    setFlags(data);
  };

  const createFlag = async (flagData: CreateFlagRequest) => {
    await client.createFlag(flagData);
    await loadFlags();
  };
  
  const updateFlag = async (id: number, flagData: UpdateFlagRequest) => {
    await client.updateFlag(id.toString(), flagData);
    await loadFlags();
  };
  
  const deleteFlag = async (id: number) => {
    await client.deleteFlag(id.toString());
    await loadFlags();
  };
  
  const toggleFlag = async (id: number, currentStatus: boolean) => {
    await client.toggleFlag(id.toString(), currentStatus);
    await loadFlags();
  };

  return {
    data: flags,
    createFlag,
    updateFlag,
    deleteFlag,
    toggleFlag,
  };
}
