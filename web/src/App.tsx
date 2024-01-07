import { useEffect, useState } from 'react';

import { LandingData } from './types';
import { fetchLandingData } from './Utils/apiCalls';

import Header from './Components/Header';

function App() {
  const [data, setData] = useState<LandingData>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    const fetchData = async () => {
      const result = await fetchLandingData();

      if ('error' in result) {
        setError(result.error);
      } else {
        setData(result);
      }
    };

    fetchData();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <Header />
      {/* TODO render data */}
    </div>
  );
}

export default App;
