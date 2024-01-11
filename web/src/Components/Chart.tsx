import { Box, Text } from '@chakra-ui/react';
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { LandingData } from '../types';

/**
 * TODO: refactor
 */
const Chart = ({ data }: { data: LandingData }) => {
  const chartData = data.data.map((item) => {
    return { name: item.Year, emissions: item.Emissions, land: item.Land };
  });

  return (
    <Box
      width={'100%'}
      height={'100%'}
      p={4}
      pr={8}
      borderWidth={1}
      borderRadius={'lg'}
      overflow={'hidden'}
      bg={'white'}
    >
      <ResponsiveContainer width="100%" height="100%" maxHeight={400}>
        <LineChart
          data={chartData}
          margin={{
            top: 5,
            right: 20,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid stroke={'#ccc'} strokeDasharray={'5 5'} />
          <XAxis dataKey="name" dy={10} />
          <YAxis
            yAxisId="left"
            orientation="left"
            tickFormatter={(value) => `${value / 1000000}`}
            label={{
              value: 'Millions',
              angle: -90,
              position: 'insideLeft',
              dy: 25,
            }}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            tickFormatter={(value) => `${value / 1000000}`}
            label={{
              value: 'Millions',
              angle: -90,
              position: 'insideRight',
              dy: -25,
            }}
          />
          <Tooltip />
          <Line
            type={'monotone'}
            yAxisId={'left'}
            dataKey={'emissions'}
            stroke={'#8884d8'}
          />
          <Line
            type={'monotone'}
            yAxisId={'right'}
            dataKey={'land'}
            stroke={'#82ca9d'}
          />
        </LineChart>
      </ResponsiveContainer>
      <Box pt={6} px={4}>
        <Text fontSize={'xl'} fontWeight={'medium'} mb={2}>
          {data.title}
        </Text>
        <Text fontSize={'md'} mb={4}>
          {data.description}
        </Text>
      </Box>
    </Box>
  );
};

export default Chart;
