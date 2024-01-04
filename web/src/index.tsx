import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { Box, ChakraProvider, extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    brand: {
      500: '#008000',
      700: '#004d00',
    },
  },
  components: {
    // NOTE: POC for customizing components, can be removed later
    Button: {
      baseStyle: {
        color: 'white',
        backgroundColor: 'brand.500',
        _hover: {
          backgroundColor: 'brand.700',
        },
      },
      defaultProps: {
        colorScheme: 'brand',
      },
    },
  },
});

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement,
);
root.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <Box minH="100vh" bgGradient="linear(to-br, green.300, green.600)">
        <App />
      </Box>
    </ChakraProvider>
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
