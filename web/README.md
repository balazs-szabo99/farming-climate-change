# Web Application for Farming Climate Change

This is the frontend web application for the Farming Climate Change project. It's built with React, a popular JavaScript library for building user interfaces.

## Installation

Before running the web application, you need to install the necessary dependencies. Make sure you have Node.js and npm installed on your machine. Then, navigate to the `web` directory and run:

`npm install`

## Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

### Available Scripts

In the project directory, you can run:

#### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

#### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

## UI

We use Chakra UI as our component library for this project. Chakra UI provides a set of accessible, reusable, and composable React components that make it easy to create websites and apps.

### Custom Theme

We have a custom theme defined in `src/index.tsx` that extends the default Chakra UI theme. The custom theme includes a POC `brand` color scheme with two shades: `500` and `700`. The `brand` color scheme is the default for all components.

### Guidelines for Developers

When creating new components, Chakra UI components should be used. This ensures consistency across the app.

When you need a color for your component, use the brand color scheme from our theme. This helps maintain a consistent look and feel across the app.

If you need to customize the style of a Chakra UI component, consider extending the theme instead of using inline styles or external CSS. This makes it easier to manage styles and promotes consistency.

## API Service

The API service is implemented in [`ApiService.ts`](web/src/Utils/ApiService.ts). This service is responsible for making all API calls from the application.

### Usage

To use the API service, you first need to import it:

```typescript
import { ApiService } from './Utils/ApiService';
```

Then, you can call the methods provided by the service. For example, to fetch landing data, you can use the fetchLandingData method:

```
const result = await ApiService.fetchLandingData();
```

This method will return a promise that resolves to the landing data. If there's an error while fetching the data, the promise will be rejected with an error message.

### Error Handling

When using the API service, you should always handle potential errors. In case of an error, the service returns an object with a `error` property.
