import { SEVERITY_COLORS, STATUS_COLORS, RISK_COLORS } from './constants';

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
