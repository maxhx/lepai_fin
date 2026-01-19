# Yay Bill Order Processor

Project containing both Python script and Vue3 web application for processing Yay bill order data.

## Linux Deployment Guide

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation and Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd lepai_fin
```

2. Install dependencies:

```bash
npm install
# OR
yarn install
```

3. Start the development server:

```bash
npm run dev
# OR
yarn dev
```

4. Build for production:

```bash
npm run build
# OR
yarn build
```

5. Preview production build:

```bash
npm run preview
# OR
yarn preview
```

### Available Scripts

- `dev`: Starts the development server
- `serve`: Alternative command to serve the application
- `build`: Builds the application for production
- `preview`: Locally previews the production build
- `python`: Runs the Python order processor script

### Production Deployment

For production deployment, run:

```bash
npm run build
```

This creates a dist folder with optimized assets. Serve these static files using any web server like Nginx, Apache, or a cloud hosting service.

### Port Configuration

The application is configured to run on port 3000 by default. If this port is unavailable, Vite will automatically select another available port.
