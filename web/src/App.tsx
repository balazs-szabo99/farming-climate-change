import { Flex, Grid } from '@chakra-ui/react';

import { fetchLandingData } from './Utils/apiCalls';

import Header from './Components/Header';
import Chart from './Components/Chart';

function App() {
  return (
    <Flex
      direction={'column'}
      minH={'100vh'}
      bgGradient="linear(to-br, green.300, green.600)"
    >
      <Header />
      <Grid
        templateColumns={{
          base: '1fr',
          lg: 'repeat(2, 1fr)',
        }}
        gridAutoRows="minmax(300px, auto)"
        gap={16}
        p={16}
      >
        <Chart fetchData={fetchLandingData} />
        {/* TODO: add rest of charts */}
      </Grid>
    </Flex>
  );
}

export default App;
