import React from 'react';

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
}
