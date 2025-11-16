import type {
  CreateFlagRequest,
  FeatureFlag,
  UpdateFlagRequest,
} from "../types/types";
export class FeatureFlagClient {
  private baseUrl: string;
  private token: string;

  constructor() {
    const baseUrl =
      import.meta.env.VITE_SERVER_BASE_URL || "http://localhost:3000";
    this.baseUrl = baseUrl;
    this.token =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZW1haWwiOiJnYWJyaWVsQGdtYWlsLmNvbSIsImV4cCI6MTc2MzQxMzA5M30.uBZTR-fJOcVTkV661fa2IXycirdqC_GmuHShaVI9Kkk";
  }

  private getAuthHeaders() {
    return {
      Authorization: `Bearer ${this.token}`,
    };
  }

  async listAllFlags(): Promise<FeatureFlag[]> {
    const response = await fetch(`${this.baseUrl}/flags`);

    if (!response.ok) {
      throw new Error(`Failed to fetch flags: ${response.statusText}`);
    }

    return await response.json();
  }

  async createFlag(flagData: CreateFlagRequest) {
    const response = await fetch(`${this.baseUrl}/flags`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...this.getAuthHeaders(),
      },
      body: JSON.stringify({ ...flagData, value: false }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create flag: ${response.statusText}`);
    }
  }

  async updateFlag(name: string, flagData: UpdateFlagRequest) {
    const response = await fetch(`${this.baseUrl}/flags/${name}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...this.getAuthHeaders(),
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
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to delete flag: ${response.statusText}`);
    }
  }

  async toggleFlag(
    name: string
  ): Promise<{ message: string; new_value: boolean }> {
    const response = await fetch(`${this.baseUrl}/flags/${name}/toggle`, {
      method: "PUT",
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle flag: ${response.statusText}`);
    }

    return await response.json();
  }
}
