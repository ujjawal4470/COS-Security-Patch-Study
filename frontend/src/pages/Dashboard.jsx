import React, { useEffect, useState } from 'react';
import { ShieldCheck, ClipboardCheck, Bug, Download } from 'lucide-react';
import DataSourceBadge from '../components/common/DataSourceBadge';
import StatusCard from '../components/common/StatusCard';
import ScoreGauge from '../components/common/ScoreGauge';
import SecurityScoreChart from '../components/charts/SecurityScoreChart';
import CISComplianceChart from '../components/charts/CISComplianceChart';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { getDashboardSummary } from '../api/client';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardSummary().then(res => { setData(res); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;
  if (!data) return <div className="text-red-400 p-6 bg-red-500/10 rounded-xl">Error loading dashboard</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 mb-1">Overview</h2>
          <p className="text-slate-400">Security posture and compliance metrics at a glance.</p>
        </div>
        <DataSourceBadge source={data.data_source} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex items-center justify-between shadow-lg">
          <div>
            <p className="text-sm font-medium text-slate-400 mb-2">Overall Security</p>
            <p className="text-xs text-slate-500">Based on recent scan</p>
          </div>
          <ScoreGauge score={data.score || 0} size="md" />
        </div>
        <StatusCard title="CIS Compliance" value={`${data.cis_compliance || 0}%`} icon={ClipboardCheck} color="emerald" />
        <StatusCard title="Total Vulnerabilities" value={data.total_cves || 0} icon={Bug} color="red" trend="down" />
        <StatusCard title="Patch Status" value={data.patch_status || 'Up to date'} icon={Download} color="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Security Score Trend</h3>
          <SecurityScoreChart data={[{ date: 'Jan', score: 60 }, { date: 'Feb', score: 75 }, { date: 'Mar', score: data.score || 85 }]} />
        </div>
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">CIS Compliance Breakdown</h3>
          <CISComplianceChart data={{ pass: data.cis_compliance, fail: 100 - data.cis_compliance, warn: 0, na: 0 }} />
        </div>
      </div>
    </div>
  );
}
