import { LandingData } from '../types';
import ApiService from './ApiService';

/**
 * Fetches the landing data.
 * @returns A promise that resolves to the landing data, or an object with an 'error' property if the request fails.
 */
export const fetchLandingData = (): Promise<
  LandingData | { error: string }
> => {
  return ApiService.get('/landing');
};
