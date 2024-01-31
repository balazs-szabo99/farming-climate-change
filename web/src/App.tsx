import { Flex, Grid } from '@chakra-ui/react';

import Header from './Components/Header';
import Chart from './Components/Chart';
import {
  fetchCerealYieldAndTemperatureData,
  fetchTemperatureAndWaterUsageData,
  fetchGreenhouseGasEmissionsAndTemperatureData,
  fetchFertilizerAndCerealYieldData,
} from './Utils/apiCalls';

function App() {
  return (
    <Flex
      direction={'column'}
      minH={'100vh'}
      bgGradient="linear(to-br, green.500, green.800)"
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
        <Chart fetchData={fetchCerealYieldAndTemperatureData} />
        <Chart fetchData={fetchTemperatureAndWaterUsageData} />
        <Chart fetchData={fetchGreenhouseGasEmissionsAndTemperatureData} />
        <Chart fetchData={fetchFertilizerAndCerealYieldData} />
      </Grid>
    </Flex>
  );
}

export default App;
