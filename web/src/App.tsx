import { useEffect, useState } from 'react';
import { Alert, Box, Center, Flex, Grid, Spinner } from '@chakra-ui/react';

import { LandingData } from './types';
import { fetchLandingData } from './Utils/apiCalls';

import Header from './Components/Header';
import Chart from './Components/Chart';

function App() {
  const [data, setData] = useState<LandingData>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    const fetchData = async () => {
      const result = await fetchLandingData();
      if ('error' in result) {
        setError(result.error);
      } else {
        setData(result);
      }
    };

    fetchData();
  }, []);

  return (
    <Flex
      direction={'column'}
      minH={'100vh'}
      bgGradient="linear(to-br, green.300, green.600)"
    >
      <Header />
      {error ? (
        <Alert status="error">{error}</Alert>
      ) : !data ? (
        <Box flex={'1'}>
          <Center h={'80vh'}>
            <Spinner color={'white'} />
          </Center>
        </Box>
      ) : (
        // TODO: replace with page
        <Grid
          templateColumns={{
            base: '1fr',
            lg: 'repeat(2, 1fr)',
          }}
          gridAutoRows="minmax(300px, auto)"
          gap={16}
          p={16}
        >
          <Chart data={data} />
        </Grid>
      )}
    </Flex>
  );
}

export default App;
