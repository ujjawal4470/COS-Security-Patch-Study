import { LayoutDashboard, Server, ShieldCheck, Lock, Network, ClipboardCheck, Box, Download, Bug, GitCompareArrows } from 'lucide-react';

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
};
