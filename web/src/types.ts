// FIXME: replace with real types
export type LandingData = {
  title: string;
  description: string;
  data: {
    'Country Name': string;
    Year: string;
    [key: string]: string | number;
  }[];
  units: {
    [key: string]: string;
  };
};
