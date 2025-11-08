type FeatureFlag = {
    id: number,
    name: string,
    description: string,
    value: boolean,
}

export default function useListFeatureFlags(): FeatureFlag[] {
    return [
        {
            id: 1,
            name: "New Ui",
            description: "Switch to the new user interface design",
            value: true,
        },
        {
            id: 2,
            name: "Export Pdf",
            description: "Enable PDF export functionality",
            value: false,
        },
        {
            id: 3,
            name: "User Avatars",
            description: "Show user profile pictures",
            value: true,
        },
        {
            id: 4,
            name: "Search Filters",
            description: "Advanced filtering options in search",
            value: true,
        },
        {
            id: 5,
            name: "Notifications",
            description: "Push notifications for important updates",
            value: false,
        }
    ]
}