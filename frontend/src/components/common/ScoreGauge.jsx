import React from 'react';

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
}
