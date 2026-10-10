import os

BASE = "/Users/ujjawalkriti/Downloads/COS-Security-Patch-Study/frontend"

files = {
"src/components/layout/Sidebar.jsx": r"""import React from 'react';
import { NavLink } from 'react-router-dom';
import { Shield } from 'lucide-react';
import { NAV_ITEMS } from '../../utils/constants';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen fixed left-0 top-0 overflow-y-auto scrollbar-dark">
      <div className="h-16 flex items-center px-6 border-b border-slate-800">
        <Shield className="w-8 h-8 text-cyan-400 mr-3" />
        <span className="text-xl font-bold text-slate-100">COS Security</span>
      </div>
      <nav className="flex-1 py-4">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center px-6 py-3 text-sm transition-colors ${
                  isActive 
                    ? 'bg-cyan-500/10 border-l-2 border-cyan-400 text-cyan-400' 
                    : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 border-l-2 border-transparent'
                }`
              }
            >
              <Icon className="w-5 h-5 mr-3" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}""",
"src/components/layout/Header.jsx": r"""import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { getVMStatus } from '../../api/client';
import { NAV_ITEMS } from '../../utils/constants';

export default function Header() {
  const [status, setStatus] = useState({ connected: false, mode: 'demo' });
  const location = useLocation();
  const currentItem = NAV_ITEMS.find(item => item.path === location.pathname) || { label: 'Dashboard' };

  useEffect(() => {
    getVMStatus().then(setStatus).catch(console.error);
  }, [location.pathname]);

  return (
    <header className="h-16 bg-slate-900/50 border-b border-slate-800 flex items-center justify-between px-8 sticky top-0 z-10 backdrop-blur-sm">
      <h1 className="text-xl font-semibold text-slate-100">{currentItem.label}</h1>
      <div className="flex items-center space-x-2 bg-slate-800/50 px-3 py-1.5 rounded-full border border-slate-700/50">
        <div className={`w-2 h-2 rounded-full ${status.connected ? 'bg-emerald-400' : 'bg-slate-400'}`} />
        <span className="text-sm font-medium text-slate-300">
          {status.connected ? 'Connected' : 'Demo Mode'}
        </span>
      </div>
    </header>
  );
}""",
"src/components/layout/DashboardLayout.jsx": r"""import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-slate-950 flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-h-screen">
        <Header />
        <main className="flex-1 p-8 overflow-x-hidden">
          <Outlet />
        </main>
      </div>
    </div>
  );
}""",
"src/components/common/DataSourceBadge.jsx": r"""import React from 'react';

export default function DataSourceBadge({ source }) {
  const isLive = source === 'live';
  return (
    <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
      isLive 
        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
        : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
    }`}>
      <span className={`w-1.5 h-1.5 rounded-full mr-1.5 ${isLive ? 'bg-emerald-400' : 'bg-amber-400 animate-pulse'}`}></span>
      {isLive ? 'LIVE DATA' : 'DEMO DATA'}
    </div>
  );
}""",
"src/components/common/StatusCard.jsx": r"""import React from 'react';

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
}""",
"src/components/common/LoadingSpinner.jsx": r"""import React from 'react';

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="w-10 h-10 border-4 border-slate-800 border-t-cyan-400 rounded-full animate-spin mb-4"></div>
      <p className="text-slate-400 font-medium">Loading...</p>
    </div>
  );
}""",
"src/components/common/ScoreGauge.jsx": r"""import React from 'react';

export default function ScoreGauge({ score, label, size = 'md' }) {
  const radius = size === 'lg' ? 60 : size === 'md' ? 40 : 25;
  const stroke = size === 'lg' ? 12 : size === 'md' ? 8 : 6;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  
  const sizeClass = size === 'lg' ? 'w-40 h-40' : size === 'md' ? 'w-24 h-24' : 'w-16 h-16';
  const textClass = size === 'lg' ? 'text-4xl' : size === 'md' ? 'text-2xl' : 'text-lg';

  let color = '#ef4444'; // red-500
  if (score >= 70) color = '#10b981'; // emerald-500
  else if (score >= 40) color = '#f59e0b'; // amber-500

  return (
    <div className="flex flex-col items-center">
      <div className={`relative flex items-center justify-center ${sizeClass}`}>
        <svg className="transform -rotate-90 w-full h-full">
          <circle
            stroke="#1e293b"
            fill="transparent"
            strokeWidth={stroke}
            r={normalizedRadius}
            cx="50%"
            cy="50%"
          />
          <circle
            stroke={color}
            fill="transparent"
            strokeWidth={stroke}
            strokeDasharray={circumference + ' ' + circumference}
            style={{ strokeDashoffset, transition: 'stroke-dashoffset 1s ease-in-out' }}
            strokeLinecap="round"
            r={normalizedRadius}
            cx="50%"
            cy="50%"
          />
        </svg>
        <span className={`absolute font-bold text-slate-100 ${textClass}`}>{score}</span>
      </div>
      {label && <span className="mt-2 text-sm font-medium text-slate-400">{label}</span>}
    </div>
  );
}"""
}

for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")

print("Part 2 complete")
