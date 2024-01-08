class ApiService {
  /**
   * Makes a GET request to the specified endpoint.
   * @param endpoint The endpoint to request. Should start with a slash ('/').
   * @returns The response data if the request is successful, or an object with an 'error' property if the request fails.
   */
  async get(endpoint: string) {
    const url = `${process.env.REACT_APP_API_URL}${endpoint}`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`Fetch error: ${error}`); // TODO: debug only, remove later
      if (error instanceof Error) {
        return { error: error.message };
      } else {
        return { error: 'An unknown error occurred' };
      }
    }
  }
}

export default new ApiService();
