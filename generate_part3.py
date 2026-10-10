import os

BASE = "/Users/ujjawalkriti/Downloads/COS-Security-Patch-Study/frontend"

files = {
"src/components/charts/SecurityScoreChart.jsx": r"""import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function SecurityScoreChart({ data }) {
  if (!data || data.length === 0) return <div className="text-slate-500 h-64 flex items-center justify-center">No data available</div>;

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }}
            itemStyle={{ color: '#06b6d4' }}
          />
          <Area type="monotone" dataKey="score" stroke="#06b6d4" strokeWidth={2} fillOpacity={1} fill="url(#colorScore)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}""",
"src/components/charts/CISComplianceChart.jsx": r"""import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = { pass: '#10b981', fail: '#ef4444', warn: '#f59e0b', na: '#64748b' };

export default function CISComplianceChart({ data }) {
  if (!data) return null;
  const chartData = [
    { name: 'Pass', value: data.pass, color: COLORS.pass },
    { name: 'Fail', value: data.fail, color: COLORS.fail },
    { name: 'Warn', value: data.warn, color: COLORS.warn },
    { name: 'N/A', value: data.na, color: COLORS.na }
  ].filter(item => item.value > 0);

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
          <Legend verticalAlign="bottom" height={36} wrapperStyle={{ fontSize: '12px', color: '#cbd5e1' }}/>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}""",
"src/components/charts/VulnerabilityTrendChart.jsx": r"""import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function VulnerabilityTrendChart({ data }) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: -20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip cursor={{ fill: '#1e293b' }} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
          <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}/>
          <Bar dataKey="critical" stackId="a" fill="#ef4444" name="Critical" />
          <Bar dataKey="high" stackId="a" fill="#f97316" name="High" />
          <Bar dataKey="medium" stackId="a" fill="#f59e0b" name="Medium" />
          <Bar dataKey="low" stackId="a" fill="#eab308" name="Low" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}""",
"src/components/charts/BeforeAfterRadar.jsx": r"""import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';

export default function BeforeAfterRadar({ before, after }) {
  const data = Object.keys(before).map(key => ({
    subject: key,
    Before: before[key] || 0,
    After: after[key] || 0,
  }));

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#64748b' }} axisLine={false} />
          <Radar name="Before" dataKey="Before" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
          <Radar name="After" dataKey="After" stroke="#10b981" fill="#10b981" fillOpacity={0.5} />
          <Legend wrapperStyle={{ fontSize: '12px' }}/>
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}""",
"src/components/charts/PatchTimelineChart.jsx": r"""import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function PatchTimelineChart({ data }) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 30, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
          <Line type="stepAfter" dataKey="cves_fixed" stroke="#06b6d4" strokeWidth={2} dot={{ fill: '#06b6d4', r: 4 }} name="CVEs Fixed" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}""",
"src/components/tables/CVETable.jsx": r"""import React from 'react';
import { getSeverityColor } from '../../utils/formatters';

export default function CVETable({ data }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-slate-700 text-slate-400 text-sm">
            <th className="py-3 px-4 font-medium">CVE ID</th>
            <th className="py-3 px-4 font-medium">Severity</th>
            <th className="py-3 px-4 font-medium">CVSS</th>
            <th className="py-3 px-4 font-medium">Description</th>
            <th className="py-3 px-4 font-medium">Status</th>
          </tr>
        </thead>
        <tbody className="text-sm">
          {data.map((row, i) => (
            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors">
              <td className="py-3 px-4 font-mono text-cyan-400">
                <a href={`https://nvd.nist.gov/vuln/detail/${row.id}`} target="_blank" rel="noreferrer" className="hover:underline">{row.id}</a>
              </td>
              <td className="py-3 px-4">
                <span className={`px-2 py-1 rounded text-xs font-semibold ${getSeverityColor(row.severity)}`}>
                  {row.severity}
                </span>
              </td>
              <td className="py-3 px-4 text-slate-300">{row.cvss}</td>
              <td className="py-3 px-4 text-slate-400 max-w-md truncate" title={row.description}>{row.description}</td>
              <td className="py-3 px-4">
                <span className={`px-2 py-1 rounded text-xs font-medium border ${row.status === 'fixed' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'}`}>
                  {row.status.toUpperCase()}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}""",
"src/components/tables/CISChecksTable.jsx": r"""import React from 'react';
import { getStatusColor } from '../../utils/formatters';

export default function CISChecksTable({ data }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-slate-700 text-slate-400 text-sm">
            <th className="py-3 px-4 font-medium">ID</th>
            <th className="py-3 px-4 font-medium">Category</th>
            <th className="py-3 px-4 font-medium">Description</th>
            <th className="py-3 px-4 font-medium">Status</th>
          </tr>
        </thead>
        <tbody className="text-sm">
          {data.map((row, i) => (
            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors">
              <td className="py-3 px-4 font-mono text-slate-300">{row.id}</td>
              <td className="py-3 px-4 text-slate-400">{row.category}</td>
              <td className="py-3 px-4 text-slate-300">{row.description}</td>
              <td className="py-3 px-4">
                <span className={`px-2 py-1 rounded text-xs font-medium border ${getStatusColor(row.status)}`}>
                  {row.status.toUpperCase()}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}""",
"src/components/tables/FirewallRulesTable.jsx": r"""import React from 'react';
import { getRiskColor } from '../../utils/formatters';

export default function FirewallRulesTable({ data }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-slate-700 text-slate-400 text-sm">
            <th className="py-3 px-4 font-medium">Name</th>
            <th className="py-3 px-4 font-medium">Direction</th>
            <th className="py-3 px-4 font-medium">Action</th>
            <th className="py-3 px-4 font-medium">Ports/Protocol</th>
            <th className="py-3 px-4 font-medium">Source</th>
            <th className="py-3 px-4 font-medium">Risk</th>
          </tr>
        </thead>
        <tbody className="text-sm">
          {data.map((row, i) => (
            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors">
              <td className="py-3 px-4 font-mono text-slate-300">{row.name}</td>
              <td className="py-3 px-4 text-slate-400">{row.direction}</td>
              <td className="py-3 px-4 text-slate-300">{row.action}</td>
              <td className="py-3 px-4 text-slate-300">{row.ports}</td>
              <td className={`py-3 px-4 font-mono ${row.source === '0.0.0.0/0' ? 'text-amber-400 font-bold' : 'text-slate-400'}`}>
                {row.source}
              </td>
              <td className="py-3 px-4">
                <span className={`px-2 py-1 rounded text-xs font-medium border ${getRiskColor(row.risk)}`}>
                  {row.risk.toUpperCase()}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}""",
"src/components/tables/HardeningActionsTable.jsx": r"""import React from 'react';

export default function HardeningActionsTable({ data, onApply }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-slate-700 text-slate-400 text-sm">
            <th className="py-3 px-4 font-medium">Category</th>
            <th className="py-3 px-4 font-medium">Title</th>
            <th className="py-3 px-4 font-medium">Status</th>
            <th className="py-3 px-4 font-medium text-right">Action</th>
          </tr>
        </thead>
        <tbody className="text-sm">
          {data.map((row, i) => (
            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors">
              <td className="py-3 px-4 text-slate-400">{row.category}</td>
              <td className="py-3 px-4 text-slate-300">{row.title}</td>
              <td className="py-3 px-4">
                <span className={`px-2 py-1 rounded text-xs font-medium border ${
                  row.status === 'applied' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                  row.status === 'skipped' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                  'bg-slate-500/10 text-slate-400 border-slate-500/20'
                }`}>
                  {row.status.toUpperCase()}
                </span>
              </td>
              <td className="py-3 px-4 text-right">
                {row.status === 'pending' && (
                  <button 
                    onClick={() => onApply(row.id)}
                    className="px-3 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded hover:bg-cyan-500/20 transition-colors"
                  >
                    Apply Fix
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}"""
}

for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")

print("Part 3 complete")
