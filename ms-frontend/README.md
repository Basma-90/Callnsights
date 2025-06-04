# Call Detail Record (CDR) Reporting Service

## Overview

The CDR Reporting Service is a comprehensive solution for tracking, analyzing, and visualizing telecommunications call records. This web application provides detailed insights into your organization's communication patterns through interactive charts and filterable reports.

## Features

- **Multi-dimensional Reports**: Analyze call data by day, service type, source, and destination
- **Interactive Charts**: Visualize data with responsive bar and pie charts
- **Filtering Options**: Filter reports by date range and service type
- **Comprehensive Metrics**: View key metrics like total usage, call count, and average call duration
- **Responsive Design**: Optimized user experience across desktop and mobile devices

## Setup Guide

### Prerequisites

- Node.js (v16 or later)
- npm (v8 or later)
- Git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Basma-90/Callnsights.git
cd cdr-reporting-service/ms-frontend
```

2. **Install dependencies**

```bash
npm install
```

3. **Configure API endpoint**

Create a `.env` file in the project root directory:
Copy from `.env.example` and fill with your own values

```
VITE_API_BASE_URL=http://your-backend-server.com/api
```

4. **Start the development server**

```bash
npm run dev
```

5. **Build for production**

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Authentication Setup

This application uses Keycloak for authentication. To configure:

1. Update the Keycloak configuration in `src/Auth/Keycloak.ts`:

```typescript
const keycloakConfig = {
  url: 'https://your-keycloak-server/auth',
  realm: 'your-realm',
  clientId: 'your-client-id'
};
```

2. Ensure the Keycloak server is accessible from your application

## API Integration

The application connects to a REST API backend. The main API endpoints used are:

- `GET /cdrs/aggregated`: Fetches aggregated call data with the following query parameters:
  - `groupBy`: Type of report to generate ('day', 'service', 'source', 'destination')
  - `startDate`: Optional filter for start date (YYYY-MM-DD)
  - `endDate`: Optional filter for end date (YYYY-MM-DD)
  - `serviceType`: Optional filter for service type

## Project Structure

```
ms-frontend/
├── public/                # Static files
├── src/
│   ├── assets/            # Images and other static resources
│   ├── Auth/              # Authentication components and services
│   ├── components/        # Reusable UI components
│   │   ├── CDRTable.tsx   # Table component for displaying CDRs
│   │   ├── Navbar.tsx     # Site navigation
│   │   └── Reports.tsx    # Reports and charts component
│   ├── pages/             # Application pages
│   │   ├── Dashboard.tsx  # Main dashboard page
│   │   ├── Home.tsx       # Landing page
│   │   └── Reports.tsx    # Reports page
│   ├── services/          # API services
│   │   └── api.ts         # API client configuration
│   ├── styles/            # CSS modules and global styles
│   ├── App.tsx            # Root component
│   └── main.tsx           # Application entry point
├── .env                   # Environment variables
├── package.json           # Project dependencies
└── vite.config.ts         # Vite configuration
```

## Usage Guide

### Generating Reports

1. Navigate to the Reports page
2. Select the desired report type: Daily, Service Type, Source, or Destination
3. Set optional date range filters
4. For Daily reports, you can filter by specific service types

### Interpreting Charts

- **Daily Usage**: Shows usage and call count per day
- **Service Type**: Displays distribution of usage across different service types
- **Source/Destination**: Visualizes usage patterns based on source/destination numbers

### Report Summary

Each report includes a summary section with:
- Total usage in seconds
- Total number of calls
- Average call duration
- Current report type

## Customization

### Adding New Chart Types

1. Update the `ReportType` type in `src/components/Reports.tsx`
2. Add a new case in the `chartData` useMemo hook
3. Modify the `renderChart` function to handle the new chart type

### Styling

The application uses CSS modules for styling. To modify the appearance:

1. Edit the relevant CSS files in the `src/styles/` directory
2. For chart customization, modify the `chartOptions` object in `Reports.tsx`
