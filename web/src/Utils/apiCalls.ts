import { LandingData } from '../types';
import ApiService from './ApiService';

export const fetchCerealYieldAndTemperatureData = async (
  country: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    '/cerealYieldAndTemperature?country=' + encodeURIComponent(country),
  );
};

export const fetchTemperatureAndWaterUsageData = async (
  country: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    '/temperatureAndWaterUsage?country=' + encodeURIComponent(country),
  );
};

export const fetchGreenhouseGasEmissionsAndTemperatureData = async (
  country: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    '/greenhouseGasEmissionsAndTemperature?country=' +
      encodeURIComponent(country),
  );
};

export const fetchFertilizerAndCerealYieldData = async (
  country: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    '/fertilizerAndCerealYield?country=' + encodeURIComponent(country),
  );
};
