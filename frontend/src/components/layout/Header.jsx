import React, { useEffect, useState } from 'react';
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
}
