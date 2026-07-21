import React, { useState } from 'react';
import { Sidebar, Menu, Icon, Segment } from 'semantic-ui-react';
import { useNavigate, useLocation, Outlet } from 'react-router-dom';

interface MenuItem {
  label: string;
  icon: string;
  path: string;
  group?: string;
}

const menuItems: MenuItem[] = [
  { label: 'Dashboard', icon: 'dashboard', path: '/dashboard' },
  { label: 'Blueprints', icon: 'file code outline', path: '/blueprints' },
  { label: 'Services', icon: 'server', path: '/services', group: 'Deployments' },
  { label: 'Environments', icon: 'cubes', path: '/environments', group: 'Deployments' },
  { label: 'Executions', icon: 'play circle', path: '/executions' },
  { label: 'Secrets', icon: 'lock', path: '/secrets', group: 'Resources' },
  { label: 'Plugins', icon: 'puzzle piece', path: '/plugins', group: 'Resources' },
  { label: 'Sites', icon: 'map marker', path: '/sites', group: 'Resources' },
  { label: 'Agents', icon: 'microchip', path: '/agents', group: 'Resources' },
  { label: 'Filters', icon: 'filter', path: '/filters', group: 'Resources' },
  { label: 'Tokens', icon: 'key', path: '/tokens', group: 'Resources' },
  { label: 'Users', icon: 'users', path: '/users', group: 'System Setup' },
  { label: 'Groups', icon: 'group', path: '/groups', group: 'System Setup' },
  { label: 'Tenants', icon: 'building', path: '/tenants', group: 'System Setup' },
  { label: 'System Health', icon: 'heartbeat', path: '/system-health', group: 'System Setup' },
  { label: 'System Logs', icon: 'file text', path: '/system-logs', group: 'System Setup' },
  { label: 'Snapshots', icon: 'camera', path: '/snapshots', group: 'System Setup' },
  { label: 'Catalog', icon: 'shopping cart', path: '/catalog' },
];

const groupedItems = menuItems.reduce((acc: any, item) => {
  const key = item.group || 'Main';
  if (!acc[key]) acc[key] = [];
  acc[key].push(item);
  return acc;
}, {} as Record<string, typeof menuItems>);

const groupOrder = ['Main', 'Deployments', 'Resources', 'System Setup'];

export default function MainLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Sidebar.Pushable as={Segment} style={{ minHeight: '100vh', border: 'none', margin: 0, borderRadius: 0 }}>
      <Sidebar
        as={Menu}
        animation="push"
        direction="left"
        visible
        inverted
        vertical
        width={collapsed ? 'thin' : 'wide'}
        style={{ background: '#1b1c1d', marginTop: 0, borderRadius: 0, overflowY: 'auto' }}
      >
        <Menu.Item style={{ justifyContent: 'space-between', alignItems: 'center' }}>
          {!collapsed && (
            <span style={{ fontWeight: 'bold', fontSize: '1.1em', color: '#00b5ad', whiteSpace: 'nowrap' }}>
              <Icon name="compass" /> Wind River Studio
            </span>
          )}
          <Icon
            name={collapsed ? 'chevron right' : 'chevron left'}
            style={{ cursor: 'pointer', color: '#aaa', marginLeft: collapsed ? 0 : 8 }}
            onClick={() => setCollapsed(!collapsed)}
          />
        </Menu.Item>

        {groupOrder.map((group) => {
          const items = groupedItems[group];
          if (!items) return null;
          return (
            <React.Fragment key={group}>
              {!collapsed && group !== 'Main' && (
                <Menu.Item style={{ fontSize: '0.75em', color: '#00b5ad', textTransform: 'uppercase', letterSpacing: '0.1em', padding: '1em 1em 0.3em', fontWeight: 'bold' }}>
                  {group}
                </Menu.Item>
              )}
              {items.map((item: MenuItem) => (
                <Menu.Item
                  key={item.path}
                  active={location.pathname === item.path}
                  onClick={() => navigate(item.path)}
                  style={{ padding: collapsed ? '0.8em 0' : '0.7em 1em', whiteSpace: 'nowrap', fontSize: '0.85em' }}
                >
                  <Icon name={item.icon as any} style={{ margin: collapsed ? '0 auto' : undefined }} />
                  {!collapsed && <span>{item.label}</span>}
                </Menu.Item>
              ))}
            </React.Fragment>
          );
        })}
      </Sidebar>

      <Sidebar.Pusher style={{ marginLeft: collapsed ? 60 : 220, transition: 'margin-left 0.3s' }}>
        <Segment basic style={{ padding: '1.5em 2em', minHeight: '100vh', background: '#f7f8fa' }}>
          <Outlet />
        </Segment>
      </Sidebar.Pusher>
    </Sidebar.Pushable>
  );
}
