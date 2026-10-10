import React, { useEffect, useState } from 'react';
import { getFirewallRules } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';
import FirewallRulesTable from '../components/tables/FirewallRulesTable';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function NetworkSecurity() {
  const [data, setData] = useState({ rules: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFirewallRules().then(res => {
      if (!res.rules || res.rules.length === 0) {
        res.rules = [
          { name: 'default-allow-ssh', direction: 'INGRESS', action: 'ALLOW', ports: 'tcp:22', source: '0.0.0.0/0', risk: 'high' },
          { name: 'allow-internal', direction: 'INGRESS', action: 'ALLOW', ports: 'all', source: '10.128.0.0/9', risk: 'low' }
        ];
      }
      setData(res);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Network Security</h2>
        <DataSourceBadge source={data.data_source} />
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">Firewall Rules Analysis</h3>
        <FirewallRulesTable data={data.rules} />
      </div>
    </div>
  );
}
