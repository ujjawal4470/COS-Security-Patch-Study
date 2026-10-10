import React, { useEffect, useState } from 'react';
import { getCurrentVersion, getPatchHistory } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import PatchTimelineChart from '../components/charts/PatchTimelineChart';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function PatchManagement() {
  const [data, setData] = useState({ version: 'M101', history: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getCurrentVersion(), getPatchHistory()]).then(([ver, hist]) => {
      setData({ 
        version: ver.version || 'M101', 
        history: hist.history?.length ? hist.history : [{date: '2023-01', cves_fixed: 5}, {date: '2023-02', cves_fixed: 12}, {date: '2023-03', cves_fixed: 3}] 
      });
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Patch Management</h2>
        <DataSourceBadge source="demo" />
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Current OS Milestone</h3>
        <div className="text-3xl font-bold text-cyan-400">{data.version}</div>
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Patch History & CVE Fixes</h3>
        <PatchTimelineChart data={data.history} />
      </div>
    </div>
  );
}
