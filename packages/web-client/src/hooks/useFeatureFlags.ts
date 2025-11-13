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
  
  const updateFlag = async (name: string, flagData: UpdateFlagRequest) => {
    await client.updateFlag(name, flagData);
    await loadFlags();
  };
  
  const deleteFlag = async (name: string) => {
    await client.deleteFlag(name);
    await loadFlags();
  };
  
  const toggleFlag = async (name: string) => {
    await client.toggleFlag(name);
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
