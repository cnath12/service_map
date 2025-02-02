import React, { useEffect, useState, useCallback } from 'react';
import { ServiceMap, LoadingSpinner, ErrorMessage } from './components';
import { ServiceConnection } from './types';
import { serviceMapApi } from './services/api';

function App() {
  const [connections, setConnections] = useState<ServiceConnection[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [minScore, setMinScore] = useState(0.1);
  const [isPolling, setIsPolling] = useState(true);

  const fetchServiceMap = useCallback(async () => {
    try {
      setError(null);
      const data = await serviceMapApi.getServiceMap(minScore);
      setConnections(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch service map data';
      setError(errorMessage);
      setIsPolling(false); // Stop polling on error
    } finally {
      setLoading(false);
    }
  }, [minScore]);

  const handleRetry = useCallback(() => {
    setLoading(true);
    setIsPolling(true);
    fetchServiceMap();
  }, [fetchServiceMap]);

  useEffect(() => {
    fetchServiceMap();
    let interval: NodeJS.Timeout;

    if (isPolling) {
      interval = setInterval(fetchServiceMap, 30000);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [fetchServiceMap, isPolling]);

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">Service Map</h1>
            {!isPolling && (
              <button
                onClick={() => setIsPolling(true)}
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
              >
                Resume Updates
              </button>
            )}
          </div>
          <div className="mt-4 flex items-center">
            <label className="mr-2">Minimum Score:</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={minScore}
              onChange={(e) => setMinScore(parseFloat(e.target.value))}
              className="w-48"
            />
            <span className="ml-2">{minScore}</span>
          </div>
        </header>

        {error && <ErrorMessage message={error} onRetry={handleRetry} />}

        {loading ? (
          <LoadingSpinner />
        ) : (
          <div className="bg-white rounded-lg shadow">
            <ServiceMap connections={connections} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;