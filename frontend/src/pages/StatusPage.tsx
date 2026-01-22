import { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';

export default function StatusPage() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const getProgressInfo = (taskStatus: string) => {
    const statusMap = {
      'None': { percent: 0, label: 'Project still in chat', eta: null },
      'Queued': { percent: 10, label: 'Started - please wait', eta: '30 mins' },
      'Creating graph': { percent: 20, label: 'Creating graph', eta: '25 mins' },
      'Preparing for research': { percent: 30, label: 'Preparing for research', eta: '20 mins' },
      'Researching': { percent: 40, label: 'Researching', eta: '15 mins' },
      'Completed': { percent: 100, label: 'Completed', eta: null }
    };

    return statusMap[taskStatus] || { percent: 0, label: taskStatus || 'Unknown status', eta: null };
  };

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/status/', {
        credentials: 'include'
      });
      const data = await response.json();

      if (data.status === 'success') {
        setStatus(data.message);
        setError(null);
      } else {
        setError(data.message);
      }
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch status. Please check if the server is running.');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  const progressInfo = getProgressInfo(status);
  const isComplete = progressInfo.percent === 100;
  const isInProgress = progressInfo.percent > 0 && progressInfo.percent < 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Project Status</h1>
          <p className="text-gray-600">Real-time progress tracking</p>
        </div>

        {error ? (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700 font-medium">{error}</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {isInProgress && (
                  <Loader2 className="w-6 h-6 text-indigo-600 animate-spin" />
                )}
                {isComplete && (
                  <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                )}
                <span className="text-xl font-semibold text-gray-800">
                  {progressInfo.label}
                </span>
              </div>
              <span className="text-2xl font-bold text-indigo-600">
                {progressInfo.percent}%
              </span>
            </div>

            <div className="relative">
              <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 transition-all duration-500 ease-out relative"
                  style={{ width: `${progressInfo.percent}%` }}
                >
                  {isInProgress && (
                    <div className="absolute inset-0 bg-white opacity-30 animate-pulse"></div>
                  )}
                </div>
              </div>
              
              {isInProgress && (
                <div className="absolute top-0 left-0 right-0 h-4 overflow-hidden rounded-full">
                  <div className="h-full bg-gradient-to-r from-transparent via-white to-transparent opacity-40 animate-shimmer"
                       style={{
                         width: '50%',
                         animation: 'shimmer 2s infinite',
                       }}></div>
                </div>
              )}
            </div>

            {progressInfo.eta && (
              <div className="bg-indigo-50 rounded-lg p-4 text-center">
                <p className="text-sm text-gray-600">Estimated time remaining</p>
                <p className="text-lg font-semibold text-indigo-600">{progressInfo.eta}</p>
              </div>
            )}

            {isComplete && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                <p className="text-green-800 font-semibold">🎉 Project completed successfully!</p>
              </div>
            )}

            <div className="text-center text-xs text-gray-400 mt-4">
              Auto-refreshing every 3 seconds
            </div>
          </div>
        )}
      </div>

      <style>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(200%); }
        }
        .animate-shimmer {
          animation: shimmer 2s infinite;
        }
      `}</style>
    </div>
  );
}