import React, { useState, useEffect } from 'react';
import { Server, CheckCircle, AlertTriangle } from 'lucide-react';
import { getVMStatus, connectVM, disconnectVM } from '../api/client';
import DataSourceBadge from '../components/common/DataSourceBadge';

export default function VMConnection() {
  const [status, setStatus] = useState({ connected: false, mode: 'demo' });
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ project: '', zone: 'us-central1-a', instance: '' });

  useEffect(() => {
    getVMStatus().then(setStatus);
  }, []);

  const handleConnect = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await connectVM(form.project, form.zone, form.instance);
      setStatus(res);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleDisconnect = async () => {
    setLoading(true);
    try {
      const res = await disconnectVM();
      setStatus(res);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-100">Target VM Connection</h2>
        <DataSourceBadge source={status.mode} />
      </div>

      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 shadow-lg">
        <div className="flex items-center space-x-4 mb-6">
          <div className={`p-4 rounded-full ${status.connected ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-700 text-slate-400'}`}>
            <Server className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-xl font-semibold text-slate-100">
              {status.connected ? 'Connected to COS Instance' : 'Not Connected'}
            </h3>
            <p className="text-slate-400">
              {status.connected ? 'Metrics are being pulled live from the target system.' : 'Currently using fallback demo data.'}
            </p>
          </div>
        </div>

        {status.connected ? (
          <button onClick={handleDisconnect} disabled={loading} className="px-4 py-2 bg-red-500/10 text-red-400 border border-red-500/20 rounded hover:bg-red-500/20 transition-colors">
            {loading ? 'Disconnecting...' : 'Disconnect'}
          </button>
        ) : (
          <form onSubmit={handleConnect} className="space-y-4 max-w-md">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">GCP Project ID</label>
              <input required type="text" value={form.project} onChange={e => setForm({...form, project: e.target.value})} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-cyan-500" placeholder="e.g. my-project-123" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Zone</label>
              <select value={form.zone} onChange={e => setForm({...form, zone: e.target.value})} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-cyan-500">
                <option value="us-central1-a">us-central1-a</option>
                <option value="us-east1-b">us-east1-b</option>
                <option value="europe-west1-b">europe-west1-b</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Instance Name</label>
              <input required type="text" value={form.instance} onChange={e => setForm({...form, instance: e.target.value})} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-cyan-500" placeholder="e.g. cos-test-vm" />
            </div>
            <button type="submit" disabled={loading} className="w-full px-4 py-2 bg-cyan-500 text-slate-950 font-semibold rounded-lg hover:bg-cyan-400 transition-colors">
              {loading ? 'Connecting...' : 'Connect to VM'}
            </button>
          </form>
        )}
      </div>

      <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-6">
        <h4 className="text-blue-400 font-semibold mb-2 flex items-center"><AlertTriangle className="w-5 h-5 mr-2" /> Prerequisites</h4>
        <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
          <li>Ensure gcloud CLI is authenticated on the backend server.</li>
          <li>Target VM must be running Container-Optimized OS.</li>
          <li>OS Login should be enabled for SSH access.</li>
        </ul>
      </div>
    </div>
  );
}
