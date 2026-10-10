import React from 'react';
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
}
