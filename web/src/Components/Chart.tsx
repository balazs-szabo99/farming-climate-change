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
    const { Year, 'Country Name': countryName, ...rest } = item;
    return {
      name: Year,
      ...rest,
    };
  });
  const keys = Object.keys(chartData[0] || {}).filter((key) => key !== 'name');

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
            tickFormatter={(value) => `${value}`}
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
            tickFormatter={(value) => `${value}`}
            label={{
              value: 'Millions',
              angle: -90,
              position: 'insideRight',
              dy: -25,
            }}
          />
          <Tooltip />
          {keys.map((key, index) => (
            <Line
              key={index}
              type={'monotone'}
              yAxisId={index % 2 === 0 ? 'left' : 'right'}
              dataKey={key}
              stroke={`#${((Math.random() * 0x777777 + 0x888888) | 0).toString(
                16,
              )}`}
            />
          ))}
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
