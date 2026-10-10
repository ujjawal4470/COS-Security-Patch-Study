import React from 'react';

export default function StatusCard({ title, value, subtitle, icon: Icon, trend, color = 'cyan' }) {
  const colorMap = {
    cyan: 'text-cyan-400',
    emerald: 'text-emerald-400',
    red: 'text-red-400',
    amber: 'text-amber-400',
  };
  const iconColor = colorMap[color] || colorMap.cyan;

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 hover:border-slate-600/50 transition-colors shadow-lg">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-400">{title}</p>
          <h3 className="text-3xl font-bold text-slate-100 mt-2">{value}</h3>
          {subtitle && <p className="text-sm text-slate-500 mt-1">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`p-3 bg-slate-900/50 rounded-lg ${iconColor}`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
      {trend && (
        <div className={`mt-4 text-sm ${trend === 'up' ? 'text-emerald-400' : 'text-red-400'}`}>
          {trend === 'up' ? '↑' : '↓'} from last scan
        </div>
      )}
    </div>
  );
}
