export const formatTickValue = (value: number) => {
  if (value >= 1_000_000_000)
    return formatDecimalValue(value / 1_000_000_000, 'B');
  if (value >= 1_000_000) return formatDecimalValue(value / 1_000_000, 'M');
  if (value >= 1_000) return formatDecimalValue(value / 1_000, 'K');
  return value.toString();
};

const formatDecimalValue = (value: number, suffix: string) => {
  const fixedValue = value.toFixed(2);
  return fixedValue.endsWith('.00')
    ? `${value.toFixed(0)}${suffix}`
    : `${fixedValue}${suffix}`;
};
