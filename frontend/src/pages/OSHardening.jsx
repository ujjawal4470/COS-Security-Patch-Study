import React, { useEffect, useState } from 'react';
import { getHardeningRecommendations, applyHardening } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import StatusCard from '../components/common/StatusCard';
import HardeningActionsTable from '../components/tables/HardeningActionsTable';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function OSHardening() {
  const [data, setData] = useState({ actions: [] });
  const [loading, setLoading] = useState(true);

  const fetchActions = () => {
    setLoading(true);
    getHardeningRecommendations().then(res => {
      // Mock some data if empty
      if (!res.actions || res.actions.length === 0) {
        res.actions = [
          { id: 1, category: 'Network', title: 'Disable IP Forwarding', status: 'pending' },
          { id: 2, category: 'Auth', title: 'Enforce Password Complexity', status: 'applied' }
        ];
      }
      setData(res);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => { fetchActions(); }, []);

  const handleApply = async (id) => {
    await applyHardening(id);
    fetchActions();
  };

  if (loading) return <LoadingSpinner />;

  const appliedCount = data.actions.filter(a => a.status === 'applied').length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">OS Hardening</h2>
        <DataSourceBadge source={data.data_source} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatusCard title="Total Actions" value={data.actions.length} color="cyan" />
        <StatusCard title="Applied Fixes" value={appliedCount} color="emerald" />
        <StatusCard title="Pending Review" value={data.actions.length - appliedCount} color="amber" />
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-100">Recommended Hardening Actions</h3>
          <div className="text-sm text-slate-400">Progress: {Math.round((appliedCount/data.actions.length)*100 || 0)}%</div>
        </div>
        <div className="w-full bg-slate-900 rounded-full h-2.5 mb-6 border border-slate-700">
          <div className="bg-cyan-500 h-2.5 rounded-full" style={{ width: `${(appliedCount/data.actions.length)*100 || 0}%` }}></div>
        </div>
        <HardeningActionsTable data={data.actions} onApply={handleApply} />
      </div>
    </div>
  );
}
