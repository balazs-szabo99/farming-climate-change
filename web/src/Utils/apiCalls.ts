import { LandingData } from '../types';
import ApiService from './ApiService';

export const fetchEmissionsAndLandData = async (
  country: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    '/emissionsAndLandData?country=' + encodeURIComponent(country),
  );
};

export const fetchEmissionAndCerealYieldData = async (
  country: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    '/emissionAndCerealYieldData?country=' + encodeURIComponent(country),
  );
};

export const fetchPopulationAndArableLandData = async (
  country: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    '/populationAndArableLand?country=' + encodeURIComponent(country),
  );
};
