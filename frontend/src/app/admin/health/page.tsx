"use client";

import React, { useEffect, useState } from 'react';
import api from '@/services/api';

interface HealthData {
  status: string;
  components: Record<string, string>;
}

export default function AdminHealthPage() {
  const [data, setData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = async () => {
    try {
      setLoading(true);
      const response = await api.get('/health');
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch system health status.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-black text-gray-900 dark:text-white">System Health</h1>
            <p className="text-gray-500 mt-1">Real-time status of backend services and infrastructure</p>
          </div>
          <button 
            onClick={fetchHealth}
            className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:bg-gray-50 transition-colors flex items-center gap-2"
          >
            <svg className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-100 text-red-600 rounded-2xl text-sm font-medium">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <HealthCard 
            name="Overall Status" 
            status={data?.status || 'unknown'} 
            loading={loading}
          />
        </div>

        <div className="mt-8">
          <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">Core Components</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data ? Object.entries(data.components).map(([name, status]) => (
              <HealthCard 
                key={name} 
                name={name.charAt(0).toUpperCase() + name.slice(1)} 
                status={status} 
              />
            )) : (
              [1, 2, 3].map(i => <div key={i} className="h-32 bg-gray-100 dark:bg-gray-800 animate-pulse rounded-3xl" />)
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function HealthCard({ name, status, loading }: { name: string; status: string; loading?: boolean }) {
  const isHealthy = status === 'healthy';
  const isWarning = status === 'no_workers_running';
  
  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 relative overflow-hidden">
      <div className="flex justify-between items-start mb-4">
        <h4 className="font-bold text-gray-900 dark:text-white">{name}</h4>
        <div className={`h-2.5 w-2.5 rounded-full ${
          loading ? 'bg-gray-300 animate-pulse' :
          isHealthy ? 'bg-green-500' :
          isWarning ? 'bg-yellow-500' : 'bg-red-500'
        }`} />
      </div>
      <div className="mt-auto">
        <p className={`text-2xl font-black ${
          loading ? 'text-gray-300' :
          isHealthy ? 'text-green-600' :
          isWarning ? 'text-yellow-600' : 'text-red-600'
        }`}>
          {loading ? '---' : status.toUpperCase()}
        </p>
      </div>
      {isHealthy && (
        <div className="absolute -right-4 -bottom-4 opacity-5 text-green-600">
          <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 24 24">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
          </svg>
        </div>
      )}
    </div>
  );
}
捉
