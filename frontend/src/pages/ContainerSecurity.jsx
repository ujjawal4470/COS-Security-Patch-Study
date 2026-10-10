import React, { useEffect, useState } from 'react';
import { getDockerInfo, getRunningContainers } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function ContainerSecurity() {
  const [data, setData] = useState({ info: {}, containers: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getDockerInfo(), getRunningContainers()]).then(([info, containers]) => {
      setData({ info, containers: containers || [] });
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Container Security</h2>
        <DataSourceBadge source={data.info.data_source || 'demo'} />
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Docker Daemon Info</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div><span className="text-slate-500">Version:</span> <span className="text-slate-200 ml-2">{data.info.version || '20.10.x'}</span></div>
          <div><span className="text-slate-500">Storage Driver:</span> <span className="text-slate-200 ml-2">overlay2</span></div>
        </div>
      </div>
    </div>
  );
}
