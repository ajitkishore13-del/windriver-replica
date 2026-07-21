import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import BlueprintsPage from './pages/BlueprintsPage';
import ExecutionsPage from './pages/ExecutionsPage';
import SecretsPage from './pages/SecretsPage';
import PluginsPage from './pages/PluginsPage';
import SitesPage from './pages/SitesPage';
import AgentsPage from './pages/AgentsPage';
import FiltersPage from './pages/FiltersPage';
import TokensPage from './pages/TokensPage';
import UsersPage from './pages/UsersPage';
import GroupsPage from './pages/GroupsPage';
import TenantsPage from './pages/TenantsPage';
import SystemHealthPage from './pages/SystemHealthPage';
import SystemLogsPage from './pages/SystemLogsPage';
import SnapshotsPage from './pages/SnapshotsPage';
import CatalogPage from './pages/CatalogPage';
import ServicesPage from './pages/ServicesPage';
import EnvironmentsPage from './pages/EnvironmentsPage';
import { isAuthenticated } from './api/client';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  if (!isAuthenticated()) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/blueprints" element={<BlueprintsPage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/environments" element={<EnvironmentsPage />} />
          <Route path="/executions" element={<ExecutionsPage />} />
          <Route path="/secrets" element={<SecretsPage />} />
          <Route path="/plugins" element={<PluginsPage />} />
          <Route path="/sites" element={<SitesPage />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/filters" element={<FiltersPage />} />
          <Route path="/tokens" element={<TokensPage />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/groups" element={<GroupsPage />} />
          <Route path="/tenants" element={<TenantsPage />} />
          <Route path="/system-health" element={<SystemHealthPage />} />
          <Route path="/system-logs" element={<SystemLogsPage />} />
          <Route path="/snapshots" element={<SnapshotsPage />} />
          <Route path="/catalog" element={<CatalogPage />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
