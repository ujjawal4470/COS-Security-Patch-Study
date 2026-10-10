import React from 'react';

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="w-10 h-10 border-4 border-slate-800 border-t-cyan-400 rounded-full animate-spin mb-4"></div>
      <p className="text-slate-400 font-medium">Loading...</p>
    </div>
  );
}
