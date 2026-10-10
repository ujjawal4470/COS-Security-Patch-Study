import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = { pass: '#10b981', fail: '#ef4444', warn: '#f59e0b', na: '#64748b' };

export default function CISComplianceChart({ data }) {
  if (!data) return null;
  const chartData = [
    { name: 'Pass', value: data.pass, color: COLORS.pass },
    { name: 'Fail', value: data.fail, color: COLORS.fail },
    { name: 'Warn', value: data.warn, color: COLORS.warn },
    { name: 'N/A', value: data.na, color: COLORS.na }
  ].filter(item => item.value > 0);

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
          <Legend verticalAlign="bottom" height={36} wrapperStyle={{ fontSize: '12px', color: '#cbd5e1' }}/>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
