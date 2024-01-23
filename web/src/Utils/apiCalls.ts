import { LandingData } from '../types';
import ApiService from './ApiService';

/**
 * Fetches the landing data.
 * @returns A promise that resolves to the landing data, or an object with an 'error' property if the request fails.
 */
// FIXME: create seperate api calls for each chart
export const fetchLandingData = async (
  country?: string,
): Promise<LandingData | { error: string }> => {
  return ApiService.get(
    country ? '/landing?country=' + encodeURIComponent(country) : '/landing',
  );
};
