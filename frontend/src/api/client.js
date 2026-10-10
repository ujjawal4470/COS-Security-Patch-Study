import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api'
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
