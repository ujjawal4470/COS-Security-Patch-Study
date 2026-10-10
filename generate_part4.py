import os

BASE = "/Users/ujjawalkriti/Downloads/COS-Security-Patch-Study/frontend"

files = {
"src/pages/Dashboard.jsx": r"""import React, { useEffect, useState } from 'react';
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
}""",
"src/pages/VMConnection.jsx": r"""import React, { useState, useEffect } from 'react';
import { Server, CheckCircle, AlertTriangle } from 'lucide-react';
import { getVMStatus, connectVM, disconnectVM } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';

export default function VMConnection() {
  const [status, setStatus] = useState({ connected: false, mode: 'demo' });
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ project: '', zone: 'us-central1-a', instance: '' });

  useEffect(() => {
    getVMStatus().then(setStatus);
  }, []);

  const handleConnect = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await connectVM(form.project, form.zone, form.instance);
      setStatus(res);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleDisconnect = async () => {
    setLoading(true);
    try {
      const res = await disconnectVM();
      setStatus(res);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Target VM Connection</h2>
        <DataSourceBadge source={status.mode} />
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <div className="flex items-center space-x-4 mb-6">
          <div className={`p-4 rounded-full ${status.connected ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-700 text-slate-400'}`}>
            <Server className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-xl font-semibold text-slate-100">
              {status.connected ? 'Connected to COS Instance' : 'Not Connected'}
            </h3>
            <p className="text-slate-400">
              {status.connected ? 'Metrics are being pulled live from the target system.' : 'Currently using fallback demo data.'}
            </p>
          </div>
        </div>

        {status.connected ? (
          <button onClick={handleDisconnect} disabled={loading} className="px-4 py-2 bg-red-500/10 text-red-400 border border-red-500/20 rounded hover:bg-red-500/20 transition-colors">
            {loading ? 'Disconnecting...' : 'Disconnect'}
          </button>
        ) : (
          <form onSubmit={handleConnect} className="space-y-4 max-w-md">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">GCP Project ID</label>
              <input required type="text" value={form.project} onChange={e => setForm({...form, project: e.target.value})} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-cyan-500" placeholder="e.g. my-project-123" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Zone</label>
              <select value={form.zone} onChange={e => setForm({...form, zone: e.target.value})} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-cyan-500">
                <option value="us-central1-a">us-central1-a</option>
                <option value="us-east1-b">us-east1-b</option>
                <option value="europe-west1-b">europe-west1-b</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Instance Name</label>
              <input required type="text" value={form.instance} onChange={e => setForm({...form, instance: e.target.value})} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-cyan-500" placeholder="e.g. cos-test-vm" />
            </div>
            <button type="submit" disabled={loading} className="w-full px-4 py-2 bg-cyan-500 text-slate-950 font-semibold rounded-lg hover:bg-cyan-400 transition-colors">
              {loading ? 'Connecting...' : 'Connect to VM'}
            </button>
          </form>
        )}
      </div>

      <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-6">
        <h4 className="text-blue-400 font-semibold mb-2 flex items-center"><AlertTriangle className="w-5 h-5 mr-2" /> Prerequisites</h4>
        <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
          <li>Ensure gcloud CLI is authenticated on the backend server.</li>
          <li>Target VM must be running Container-Optimized OS.</li>
          <li>OS Login should be enabled for SSH access.</li>
        </ul>
      </div>
    </div>
  );
}""",
"src/pages/SecurityAssessment.jsx": r"""import React, { useEffect, useState } from 'react';
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
}""",
"src/pages/OSHardening.jsx": r"""import React, { useEffect, useState } from 'react';
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
}""",
"src/pages/NetworkSecurity.jsx": r"""import React, { useEffect, useState } from 'react';
import { getFirewallRules } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import FirewallRulesTable from '../components/tables/FirewallRulesTable';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function NetworkSecurity() {
  const [data, setData] = useState({ rules: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFirewallRules().then(res => {
      if (!res.rules || res.rules.length === 0) {
        res.rules = [
          { name: 'default-allow-ssh', direction: 'INGRESS', action: 'ALLOW', ports: 'tcp:22', source: '0.0.0.0/0', risk: 'high' },
          { name: 'allow-internal', direction: 'INGRESS', action: 'ALLOW', ports: 'all', source: '10.128.0.0/9', risk: 'low' }
        ];
      }
      setData(res);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Network Security</h2>
        <DataSourceBadge source={data.data_source} />
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Firewall Rules Analysis</h3>
        <FirewallRulesTable data={data.rules} />
      </div>
    </div>
  );
}"""
}

for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")

print("Part 4 complete")
