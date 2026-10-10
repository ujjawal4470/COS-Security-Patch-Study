import React from 'react';
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
}
