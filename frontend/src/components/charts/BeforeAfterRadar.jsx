import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';

export default function BeforeAfterRadar({ before, after }) {
  const data = Object.keys(before).map(key => ({
    subject: key,
    Before: before[key] || 0,
    After: after[key] || 0,
  }));

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#64748b' }} axisLine={false} />
          <Radar name="Before" dataKey="Before" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
          <Radar name="After" dataKey="After" stroke="#10b981" fill="#10b981" fillOpacity={0.5} />
          <Legend wrapperStyle={{ fontSize: '12px' }}/>
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
