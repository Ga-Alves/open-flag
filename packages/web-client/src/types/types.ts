export type FeatureFlag = {
  id: number;
  name: string;
  description: string;
  status: boolean;
}

export type CreateFlagRequest = {
  name: string;
  description: string;
}

export type UpdateFlagRequest = {
  name?: string;
  description?: string;
  status?: boolean;
}

export type CheckFlagResponse = {
  name: string;
  status: boolean;
}
