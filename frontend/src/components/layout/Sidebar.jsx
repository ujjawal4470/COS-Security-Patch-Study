import React from 'react';
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
}
