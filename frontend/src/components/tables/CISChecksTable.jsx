import React from 'react';
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
}
