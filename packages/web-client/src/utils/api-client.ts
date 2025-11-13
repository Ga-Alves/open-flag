import { FeatureFlagList } from "./mockData";
import type {
  FeatureFlag,
  CheckFlagResponse,
  CreateFlagRequest,
  UpdateFlagRequest,
} from "../types/types";

export class FeatureFlagClient {
  private baseUrl: string;

  constructor() {
    const baseUrl =
      import.meta.env.VITE_SERVER_BASE_URL || "http://localhost:3000";

    this.baseUrl = baseUrl;
  }

  async listAllFlags(): Promise<FeatureFlag[]> {
    const response = await fetch(`${this.baseUrl}/flags`);

    if (!response.ok) {
      throw new Error(`Failed to fetch flags: ${response.statusText}`);
    }

    const res = await response.json()
  
    return res
  }

  async createFlag(flagData: CreateFlagRequest) {
    // const response = await fetch(`${this.baseUrl}/flags`, {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify(flagData),
    // });
    // if (!response.ok) {
    //   throw new Error(`Failed to create flag: ${response.statusText}`);
    // }
  }

  async updateFlag(name: string, flagData: UpdateFlagRequest) {
    const response = await fetch(`${this.baseUrl}/flags/${name}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(flagData),
    });
    if (!response.ok) {
      throw new Error(`Failed to update flag: ${response.statusText}`);
    }
  }

  async deleteFlag(id: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/flags/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new Error(`Failed to delete flag: ${response.statusText}`);
    }
  }

  async toggleFlag(id: string, currentStatus: boolean) {
    this.updateFlag(id, { value: !currentStatus });
  }
}
