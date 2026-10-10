import React, { useEffect, useState } from 'react';
import { getLatestAssessment, runAssessment } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import ScoreGauge from '../components/common/ScoreGauge';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function SecurityAssessment() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  const fetchAssessment = () => {
    setLoading(true);
    getLatestAssessment().then(res => { setData(res); setLoading(false); }).catch(() => setLoading(false));
  };

  useEffect(() => { fetchAssessment(); }, []);

  const handleRun = async () => {
    setRunning(true);
    try {
      await runAssessment('Manual');
      fetchAssessment();
    } catch(e) { console.error(e); }
    setRunning(false);
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Security Assessment</h2>
        <div className="flex items-center space-x-4">
          <DataSourceBadge source={data?.data_source} />
          <button onClick={handleRun} disabled={running} className="px-4 py-2 bg-cyan-500 text-slate-950 font-semibold rounded hover:bg-cyan-400 transition-colors">
            {running ? 'Running...' : 'Run Assessment Now'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg flex flex-col items-center justify-center">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Overall Score</h3>
          <ScoreGauge score={data?.score || 0} size="lg" />
        </div>
        <div className="col-span-2 bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">System Information</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div><span className="text-slate-500">OS Name:</span> <span className="text-slate-200 ml-2">{data?.os_info?.name || 'Unknown'}</span></div>
            <div><span className="text-slate-500">Version:</span> <span className="text-slate-200 ml-2">{data?.os_info?.version || 'Unknown'}</span></div>
            <div><span className="text-slate-500">Kernel:</span> <span className="text-slate-200 ml-2">{data?.os_info?.kernel || 'Unknown'}</span></div>
            <div><span className="text-slate-500">Architecture:</span> <span className="text-slate-200 ml-2">{data?.os_info?.arch || 'Unknown'}</span></div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Sysctl Findings (Simulated)</h3>
        <p className="text-slate-400 text-sm mb-4">Key kernel parameters analyzed during assessment.</p>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-700 text-slate-400 text-sm">
                <th className="py-2 px-4">Parameter</th>
                <th className="py-2 px-4">Current Value</th>
                <th className="py-2 px-4">Recommended</th>
                <th className="py-2 px-4">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-slate-800/50">
                <td className="py-2 px-4 font-mono text-sm text-slate-300">net.ipv4.ip_forward</td>
                <td className="py-2 px-4 text-slate-400">1</td>
                <td className="py-2 px-4 text-slate-400">0</td>
                <td className="py-2 px-4"><span className="text-amber-400 text-xs border border-amber-500/30 px-2 py-1 rounded bg-amber-500/10">WARN</span></td>
              </tr>
              <tr>
                <td className="py-2 px-4 font-mono text-sm text-slate-300">net.ipv4.conf.all.accept_source_route</td>
                <td className="py-2 px-4 text-slate-400">0</td>
                <td className="py-2 px-4 text-slate-400">0</td>
                <td className="py-2 px-4"><span className="text-emerald-400 text-xs border border-emerald-500/30 px-2 py-1 rounded bg-emerald-500/10">PASS</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
