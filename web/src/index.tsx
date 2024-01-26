import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import {
  ChakraProvider,
  extendTheme,
  withDefaultColorScheme,
} from '@chakra-ui/react';

const theme = extendTheme(
  {
    colors: {
      brand: {
        100: '#ccffcc',
        300: '#99ff99',
        500: '#008000',
        700: '#004d00',
      },
    },
    components: {
      // NOTE: POC for customizing components, can be removed later
      Button: {
        baseStyle: {
          _hover: {
            backgroundColor: 'brand.700',
          },
        },
      },
    },
  },
  withDefaultColorScheme({ colorScheme: 'brand' }),
);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement,
);
root.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
