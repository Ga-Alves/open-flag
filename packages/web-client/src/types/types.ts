export type FeatureFlag = {
  name: string;
  description: string;
  status: boolean;
  usage_timestamps: number[]
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
