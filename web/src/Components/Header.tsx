import { FC } from 'react';
import { Flex, Text } from '@chakra-ui/react';

const Header: FC = () => {
  return (
    <Flex
      as="header"
      justifyContent="center"
      alignItems="center"
      padding="1.5rem"
      bg="green.700"
      data-testid={'header'}
    >
      <Text fontSize="2xl" fontWeight="bold" color="white">
        AgroAware - Farming Climate Change
      </Text>
    </Flex>
  );
};

export default Header;
