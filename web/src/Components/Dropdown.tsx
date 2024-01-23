import {
  Box,
  Button,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
} from '@chakra-ui/react';
import { FC, useEffect, useRef, useState } from 'react';
import { BsChevronDown, BsChevronUp } from 'react-icons/bs';

interface DropdownProps {
  selected: string;
  options: string[];
  onChange: (selected: string) => void;
}

const Dropdown: FC<DropdownProps> = ({ selected, options, onChange }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const handleLimitChange = (selected: string) => {
    onChange(selected);
    setIsOpen(false);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (!dropdownRef.current?.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <Box position="relative">
      <Menu>
        <MenuButton
          as={Button}
          rightIcon={isOpen ? <BsChevronUp /> : <BsChevronDown />}
          fontSize={'sm'}
          px={2}
        >
          {selected}
        </MenuButton>
        <MenuList>
          {options.map((option) => (
            <MenuItem
              key={option}
              onClick={() => handleLimitChange(option)}
              bg={option === selected ? 'brand.300' : undefined}
            >
              {option}
            </MenuItem>
          ))}
        </MenuList>
      </Menu>
    </Box>
  );
};

export default Dropdown;
