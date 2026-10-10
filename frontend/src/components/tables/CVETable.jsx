import React from 'react';
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
}
