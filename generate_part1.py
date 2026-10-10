import os

BASE = "/Users/ujjawalkriti/Downloads/COS-Security-Patch-Study/frontend"

files = {
"package.json": r"""{
  "name": "cos-security-dashboard",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "recharts": "^2.10.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.0"
  }
}""",
"vite.config.js": r"""import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});""",
"tailwind.config.js": r"""/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        slate: {
          950: '#020617',
          900: '#0f172a',
          800: '#1e293b',
          700: '#334155',
        }
      }
    },
  },
  plugins: [],
};""",
"postcss.config.js": r"""export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};""",
"index.html": r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>COS Security Dashboard</title>
  </head>
  <body class="bg-slate-950 text-slate-100">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>""",
"Dockerfile": r"""FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]""",
"nginx.conf": r"""server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}""",
"src/main.jsx": r"""import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);""",
"src/App.jsx": r"""import React from 'react';
import { Routes, Route } from 'react-router-dom';
import DashboardLayout from './components/layout/DashboardLayout';
import Dashboard from './pages/Dashboard';
import VMConnection from './pages/VMConnection';
import SecurityAssessment from './pages/SecurityAssessment';
import OSHardening from './pages/OSHardening';
import NetworkSecurity from './pages/NetworkSecurity';
import CISCompliance from './pages/CISCompliance';
import ContainerSecurity from './pages/ContainerSecurity';
import PatchManagement from './pages/PatchManagement';
import CVEStudy from './pages/CVEStudy';
import BeforeAfterComparison from './pages/BeforeAfterComparison';

export default function App() {
  return (
    <Routes>
      <Route element={<DashboardLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/vm-connection" element={<VMConnection />} />
        <Route path="/assessment" element={<SecurityAssessment />} />
        <Route path="/hardening" element={<OSHardening />} />
        <Route path="/network" element={<NetworkSecurity />} />
        <Route path="/cis-compliance" element={<CISCompliance />} />
        <Route path="/container-security" element={<ContainerSecurity />} />
        <Route path="/patches" element={<PatchManagement />} />
        <Route path="/cve-study" element={<CVEStudy />} />
        <Route path="/comparison" element={<BeforeAfterComparison />} />
      </Route>
    </Routes>
  );
}""",
"src/index.css": r"""@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .scrollbar-dark::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  .scrollbar-dark::-webkit-scrollbar-track {
    background: #0f172a; 
  }
  .scrollbar-dark::-webkit-scrollbar-thumb {
    background: #334155; 
    border-radius: 4px;
  }
  .scrollbar-dark::-webkit-scrollbar-thumb:hover {
    background: #475569; 
  }
}
body {
  @apply scrollbar-dark;
}""",
"src/api/client.js": r"""import axios from 'axios';

const api = axios.create({
  baseURL: '/api'
});

export const getDashboardSummary = () => api.get('/dashboard/summary').then(res => res.data).catch(() => ({ data_source: 'demo', score: 85, cis_compliance: 78, total_cves: 12, patch_status: '2 Updates Available' }));
export const getVMStatus = () => api.get('/vm/status').then(res => res.data).catch(() => ({ connected: false, mode: 'demo' }));
export const connectVM = (project, zone, instance) => api.post('/vm/connect', { project, zone, instance }).then(res => res.data);
export const disconnectVM = () => api.post('/vm/disconnect').then(res => res.data);
export const runAssessment = (label) => api.post('/assessment/run', { label }).then(res => res.data);
export const getLatestAssessment = () => api.get('/assessment/latest').then(res => res.data).catch(() => ({ data_source: 'demo', score: 75, os_info: { name: 'COS', version: '101' } }));
export const getAssessmentHistory = () => api.get('/assessment/history').then(res => res.data);
export const getHardeningRecommendations = () => api.get('/hardening/recommendations').then(res => res.data).catch(() => ({ data_source: 'demo', actions: [] }));
export const getHardeningStatus = () => api.get('/hardening/status').then(res => res.data);
export const applyHardening = (actionId) => api.post('/hardening/apply', { actionId }).then(res => res.data);
export const getFirewallRules = () => api.get('/network/firewall').then(res => res.data).catch(() => ({ data_source: 'demo', rules: [] }));
export const getNetworkAnalysis = () => api.get('/network/analysis').then(res => res.data);
export const runCISChecks = () => api.post('/cis/run').then(res => res.data);
export const getLatestCIS = () => api.get('/cis/latest').then(res => res.data).catch(() => ({ data_source: 'demo', compliance: 80, checks: [] }));
export const getCISBenchmarks = () => api.get('/cis/benchmarks').then(res => res.data);
export const getDockerInfo = () => api.get('/container/info').then(res => res.data).catch(() => ({ data_source: 'demo', version: '20.10', containers: [] }));
export const getRunningContainers = () => api.get('/container/running').then(res => res.data);
export const getContainerSecurityChecks = () => api.get('/container/security').then(res => res.data);
export const getCurrentVersion = () => api.get('/patches/current').then(res => res.data).catch(() => ({ data_source: 'demo', version: 'M101' }));
export const getPatchHistory = () => api.get('/patches/history').then(res => res.data).catch(() => ({ data_source: 'demo', history: [] }));
export const getCVEList = (page, severity) => api.get('/cve/list', { params: { page, severity } }).then(res => res.data).catch(() => ({ data_source: 'demo', cves: [] }));
export const getCVEStatistics = () => api.get('/cve/statistics').then(res => res.data).catch(() => ({ data_source: 'demo', stats: {} }));
export const getCVEDetail = (cveId) => api.get(`/cve/${cveId}`).then(res => res.data);
export const getLatestComparison = () => api.get('/comparison/latest').then(res => res.data).catch(() => ({ data_source: 'demo', before: {}, after: {} }));
export const createSnapshot = (label) => api.post('/snapshot/create', { label }).then(res => res.data);
""",
"src/utils/constants.js": r"""import { LayoutDashboard, Server, ShieldCheck, Lock, Network, ClipboardCheck, Box, Download, Bug, GitCompareArrows } from 'lucide-react';

export const NAV_ITEMS = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/vm-connection', label: 'VM Connection', icon: Server },
  { path: '/assessment', label: 'Security Assessment', icon: ShieldCheck },
  { path: '/hardening', label: 'OS Hardening', icon: Lock },
  { path: '/network', label: 'Network Security', icon: Network },
  { path: '/cis-compliance', label: 'CIS Compliance', icon: ClipboardCheck },
  { path: '/container-security', label: 'Container Security', icon: Box },
  { path: '/patches', label: 'Patch Management', icon: Download },
  { path: '/cve-study', label: 'CVE Study', icon: Bug },
  { path: '/comparison', label: 'Before vs After', icon: GitCompareArrows },
];

export const SEVERITY_COLORS = {
  CRITICAL: 'text-red-500 bg-red-500/10 border-red-500/20',
  HIGH: 'text-orange-500 bg-orange-500/10 border-orange-500/20',
  MEDIUM: 'text-amber-500 bg-amber-500/10 border-amber-500/20',
  LOW: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
  INFO: 'text-blue-400 bg-blue-400/10 border-blue-400/20',
};

export const STATUS_COLORS = {
  PASS: 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  FAIL: 'text-red-400 bg-red-400/10 border-red-400/20',
  WARN: 'text-amber-400 bg-amber-400/10 border-amber-400/20',
};

export const RISK_COLORS = {
  HIGH: 'text-red-500 bg-red-500/10 border-red-500/20',
  MEDIUM: 'text-amber-500 bg-amber-500/10 border-amber-500/20',
  LOW: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20',
};""",
"src/utils/formatters.js": r"""import { SEVERITY_COLORS, STATUS_COLORS, RISK_COLORS } from './constants';

export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
};

export const formatScore = (score) => {
  if (score >= 80) return 'text-emerald-400';
  if (score >= 50) return 'text-amber-400';
  return 'text-red-400';
};

export const getSeverityColor = (severity) => SEVERITY_COLORS[severity?.toUpperCase()] || SEVERITY_COLORS.INFO;
export const getStatusColor = (status) => STATUS_COLORS[status?.toUpperCase()] || 'text-slate-400 bg-slate-400/10 border-slate-400/20';
export const getRiskColor = (risk) => RISK_COLORS[risk?.toUpperCase()] || 'text-slate-400 bg-slate-400/10 border-slate-400/20';
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")

print("Part 1 complete")
