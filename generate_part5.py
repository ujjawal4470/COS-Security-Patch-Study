import os

BASE = "/Users/ujjawalkriti/Downloads/COS-Security-Patch-Study/frontend"

files = {
"src/pages/CISCompliance.jsx": r"""import React, { useEffect, useState } from 'react';
import { getLatestCIS, runCISChecks } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import CISChecksTable from '../components/tables/CISChecksTable';
import CISComplianceChart from '../components/charts/CISComplianceChart';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function CISCompliance() {
  const [data, setData] = useState({ compliance: 0, checks: [] });
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  const fetchCIS = () => {
    setLoading(true);
    getLatestCIS().then(res => {
      if (!res.checks || res.checks.length === 0) {
        res.checks = [
          { id: '1.1.1', category: 'Filesystem', description: 'Ensure mounting of cramfs filesystems is disabled', status: 'pass' },
          { id: '1.1.2', category: 'Filesystem', description: 'Ensure mounting of freevxfs filesystems is disabled', status: 'fail' },
          { id: '4.1.1', category: 'Network', description: 'Ensure IP forwarding is disabled', status: 'warn' }
        ];
      }
      setData(res);
      setLoading(false);
    });
  };

  useEffect(() => { fetchCIS(); }, []);

  const handleRun = async () => {
    setRunning(true);
    await runCISChecks();
    fetchCIS();
    setRunning(false);
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">CIS Compliance</h2>
        <div className="flex items-center space-x-4">
          <DataSourceBadge source={data.data_source} />
          <button onClick={handleRun} disabled={running} className="px-4 py-2 bg-cyan-500 text-slate-950 font-semibold rounded hover:bg-cyan-400 transition-colors">
            {running ? 'Running...' : 'Run CIS Checks'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg flex flex-col items-center justify-center">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Compliance Status</h3>
          <div className="text-5xl font-bold text-emerald-400">{data.compliance}%</div>
          <p className="text-slate-400 mt-2">Passed Checks</p>
        </div>
        <div className="col-span-2 bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Distribution</h3>
          <CISComplianceChart data={{ pass: 60, fail: 20, warn: 15, na: 5 }} />
        </div>
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Detailed Results</h3>
        <CISChecksTable data={data.checks} />
      </div>
    </div>
  );
}""",
"src/pages/ContainerSecurity.jsx": r"""import React, { useEffect, useState } from 'react';
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
}""",
"src/pages/PatchManagement.jsx": r"""import React, { useEffect, useState } from 'react';
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
}""",
"src/pages/CVEStudy.jsx": r"""import React, { useEffect, useState } from 'react';
import { getCVEList } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import CVETable from '../components/tables/CVETable';
import VulnerabilityTrendChart from '../components/charts/VulnerabilityTrendChart';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function CVEStudy() {
  const [data, setData] = useState({ cves: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCVEList().then(res => {
      if (!res.cves || res.cves.length === 0) {
        res.cves = [
          { id: 'CVE-2023-1234', severity: 'HIGH', cvss: 8.5, description: 'Kernel vulnerability in network stack', status: 'affected' },
          { id: 'CVE-2023-5678', severity: 'MEDIUM', cvss: 5.5, description: 'Docker daemon privilege escalation', status: 'fixed' }
        ];
      }
      setData(res);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">CVE Study & Tracking</h2>
        <DataSourceBadge source={data.data_source || 'demo'} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg lg:col-span-2">
          <h3 className="text-lg font-semibold text-slate-100 mb-4">Vulnerability Trends by Year</h3>
          <VulnerabilityTrendChart data={[
            { year: '2021', critical: 2, high: 5, medium: 10, low: 15 },
            { year: '2022', critical: 1, high: 8, medium: 12, low: 8 },
            { year: '2023', critical: 0, high: 3, medium: 5, low: 2 }
          ]} />
        </div>
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Discovered CVEs</h3>
        <CVETable data={data.cves} />
      </div>
    </div>
  );
}""",
"src/pages/BeforeAfterComparison.jsx": r"""import React, { useEffect, useState } from 'react';
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
}"""
}

for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")

print("Part 5 complete")
