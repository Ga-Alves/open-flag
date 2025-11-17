import type {
  FeatureFlag,
  CreateFlagRequest,
  UpdateFlagRequest,
} from "../types/types";

/**
 * Headers de autenticação.
 * Sempre retorna um Record<string, string> seguro.
 */
function authHeaders(): Record<string, string> {
  const token = localStorage.getItem("token");

  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
}

export class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl =
      (import.meta as any).env.VITE_SERVER_BASE_URL || "http://localhost:3000";
  }

  /**
   * Wrapper para TODAS as requisições HTTP.
   */
  private async request(url: string, options: RequestInit = {}) {
    const finalHeaders: Record<string, string> = {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(options.headers as Record<string, string> | undefined),
    };

    const response = await fetch(url, {
      ...options,
      headers: finalHeaders,
    });

    if (response.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("email");
      window.location.href = "/login";
      throw new Error("Unauthorized – token expired or invalid");
    }

    return response;
  }

  // ===============================================================
  // LOGIN
  // ===============================================================
  async login(email: string, password: string) {
    const res = await this.request(`${this.baseUrl}/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) throw new Error("Invalid email or password");

    return res.json();
  }

  // ===============================================================
  // USER REGISTRATION
  // ===============================================================
  async register(name: string, email: string, password: string) {
    const res = await this.request(`${this.baseUrl}/users`, {
      method: "POST",
      body: JSON.stringify({ name, email, password }),
    });

    if (!res.ok) throw new Error("Failed to register user");

    return res.json();
  }

  // ===============================================================
  // FLAGS
  // ===============================================================

  async listAllFlags(): Promise<FeatureFlag[]> {
    const response = await this.request(`${this.baseUrl}/flags`);

    if (!response.ok) {
      throw new Error(`Failed to fetch flags: ${response.statusText}`);
    }

    return response.json();
  }

  async createFlag(flagData: CreateFlagRequest) {
    const response = await this.request(`${this.baseUrl}/flags`, {
      method: "POST",
      body: JSON.stringify({ ...flagData, value: false }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create flag: ${response.statusText}`);
    }
  }

  async updateFlag(name: string, flagData: UpdateFlagRequest) {
    const response = await this.request(`${this.baseUrl}/flags/${name}`, {
      method: "PUT",
      body: JSON.stringify(flagData),
    });

    if (!response.ok) {
      throw new Error(`Failed to update flag: ${response.statusText}`);
    }
  }

  async deleteFlag(name: string): Promise<void> {
    const response = await this.request(`${this.baseUrl}/flags/${name}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`Failed to delete flag: ${response.statusText}`);
    }
  }

  async toggleFlag(
    name: string
  ): Promise<{ message: string; new_value: boolean }> {
    const response = await this.request(`${this.baseUrl}/flags/${name}/toggle`, {
      method: "PUT",
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle flag: ${response.statusText}`);
    }

    return response.json();
  }

  async me() {
    const res = await this.request(`${this.baseUrl}/me`);

    if (!res.ok) throw new Error("Failed to load user profile");

    return res.json();
  }

}

export const api = new ApiClient();

/**
 * Compatibilidade com código antigo.
 * Agora FeatureFlagClient apenas usa api internamente.
 */
export class FeatureFlagClient {
  listAllFlags = api.listAllFlags.bind(api);
  createFlag = api.createFlag.bind(api);
  updateFlag = api.updateFlag.bind(api);
  deleteFlag = api.deleteFlag.bind(api);
  toggleFlag = api.toggleFlag.bind(api);
}
