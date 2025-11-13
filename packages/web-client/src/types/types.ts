export type FeatureFlag = {
  name: string;
  description: string;
  value: boolean;
  usage_timestamps: number[]
}

export type CreateFlagRequest = {
  name: string;
  description: string;
}

export type UpdateFlagRequest = {
  name?: string;
  description?: string;
  value?: boolean;
}

export type CheckFlagResponse = {
  name: string;
  value: boolean;
}
