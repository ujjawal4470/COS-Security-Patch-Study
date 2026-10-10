import React, { useEffect, useState } from 'react';
import { getLatestComparison } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import BeforeAfterRadar from '../components/charts/BeforeAfterRadar';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ScoreGauge from '../components/common/ScoreGauge';

export default function BeforeAfterComparison() {
  const [data, setData] = useState({ before: {}, after: {} });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestComparison().then(res => {
      setData({
        before: { "OS Hardening": 40, "Network": 50, "CIS": 45, "Container": 60, "Patch": 70 },
        after: { "OS Hardening": 85, "Network": 90, "CIS": 80, "Container": 95, "Patch": 100 }
      });
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Before & After Hardening</h2>
        <DataSourceBadge source="demo" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg flex flex-col items-center justify-center">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Initial Posture</h3>
          <ScoreGauge score={53} size="md" />
        </div>
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg flex flex-col items-center justify-center">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Current Posture</h3>
          <ScoreGauge score={90} size="md" />
        </div>
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg flex flex-col items-center justify-center">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Improvement</h3>
          <div className="text-5xl font-bold text-emerald-400">+37%</div>
          <p className="text-slate-400 mt-2">Overall Score Delta</p>
        </div>
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Security Domain Comparison</h3>
        <BeforeAfterRadar before={data.before} after={data.after} />
      </div>
    </div>
  );
}
