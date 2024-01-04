import { FC } from 'react';
import { Flex, Text } from '@chakra-ui/react';

const Header: FC = () => {
  return (
    <Flex
      as="header"
      justifyContent="center"
      alignItems="center"
      padding="1.5rem"
      bg="green.500"
      data-testid={'header'}
    >
      <Text fontSize="2xl" fontWeight="bold" color="white">
        {/* TODO: replace with actual app name */}
        App Title
      </Text>
    </Flex>
  );
};

export default Header;
