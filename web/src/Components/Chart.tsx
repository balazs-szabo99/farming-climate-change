import { useEffect, useState } from 'react';
import { Alert, Box, Center, Spacer, Spinner, Text } from '@chakra-ui/react';
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
import { formatTickValue } from '../Utils/util';
import Dropdown from './Dropdown';

const Chart = ({
  fetchData,
}: {
  fetchData: (country: string) => Promise<LandingData | { error: string }>;
}) => {
  const [selectedCountry, setSelectedCountry] = useState('World');
  const [data, setData] = useState<LandingData>();
  const [error, setError] = useState<string>();
  const chartData = data?.data?.map((item) => {
    const { Year, 'Country Name': countryName, ...rest } = item;
    return {
      name: Year,
      ...rest,
    };
  });
  const keys = Object.keys(chartData ? chartData[0] : {}).filter(
    (key) => key !== 'name',
  );
  const dropdownOptions = ['World', 'Austria', 'Germany', 'Hungary']; // TODO: get from API

  useEffect(() => {
    const fetch = async () => {
      const result = await fetchData(selectedCountry);
      if ('error' in result) {
        setError(result.error);
      } else {
        setData(result);
      }
    };

    fetch();
  }, [fetchData, selectedCountry]);

  return (
    <Box
      width={'100%'}
      height={'100%'}
      p={4}
      borderWidth={1}
      borderRadius={'lg'}
      overflow={'hidden'}
      bg={'white'}
    >
      {error ? (
        <Alert status="error">{error}</Alert>
      ) : !data ? (
        <Box flex={'1'}>
          <Center h={'150px'}>
            <Spinner color={'brand.500'} />
          </Center>
        </Box>
      ) : (
        <>
          <Box display={'flex'} p={2} mb={4} alignItems={'center'}>
            <Text fontSize={'xl'} fontWeight={'medium'}>
              {data.title}
            </Text>
            <Spacer />
            <Dropdown
              selected={selectedCountry}
              options={dropdownOptions}
              onChange={setSelectedCountry}
            />
          </Box>
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
                tickFormatter={formatTickValue}
                label={{
                  value:
                    data.units && data.units[keys[0]]
                      ? data.units[keys[0]]
                      : '',
                  angle: -90,
                  position: 'insideLeft',
                  dx: -10,
                  style: {
                    textAnchor: 'middle',
                  },
                }}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                tickFormatter={formatTickValue}
                label={{
                  value:
                    data.units && data.units[keys[1]]
                      ? data.units[keys[1]]
                      : '',
                  angle: -90,
                  position: 'insideRight',
                  dx: 10,
                  style: {
                    textAnchor: 'middle',
                  },
                }}
              />
              <Tooltip />
              {keys.map((key, index) => (
                <Line
                  key={index}
                  type={'monotone'}
                  yAxisId={index % 2 === 0 ? 'left' : 'right'}
                  dataKey={key}
                  stroke={`#${(
                    (Math.random() * 0x777777 + 0x888888) |
                    0
                  ).toString(16)}`}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
          <Box pt={6} px={4}>
            <Text fontSize={'md'} mb={4}>
              {data.description}
            </Text>
          </Box>
        </>
      )}
    </Box>
  );
};

export default Chart;
