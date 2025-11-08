import type { FeatureFlag } from "../types/types";

export const FeatureFlagList: FeatureFlag[] = [
  {
    id: 1,
    name: "New Ui",
    description: "Switch to the new user interface design",
    status: true,
  },
  {
    id: 2,
    name: "Export Pdf",
    description: "Enable PDF export functionality",
    status: false,
  },
  {
    id: 3,
    name: "User Avatars",
    description: "Show user profile pictures",
    status: true,
  },
  {
    id: 4,
    name: "Search Filters",
    description: "Advanced filtering options in search",
    status: true,
  },
  {
    id: 5,
    name: "Notifications",
    description: "Push notifications for important updates",
    status: false,
  },
];
