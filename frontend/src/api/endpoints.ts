import api from './client';

export const endpoints = {
  status: () => api.get('/status'),
  tokens: () => api.get('/tokens'),

  blueprints: {
    list: (params?: any) => api.get('/blueprints', { params }),
    get: (id: string) => api.get(`/blueprints/${id}`),
    create: (id: string, data: any) => api.put(`/blueprints/${id}`, data),
    update: (id: string, data: any) => api.patch(`/blueprints/${id}`, data),
    delete: (id: string) => api.delete(`/blueprints/${id}`),
    setVisibility: (id: string, visibility: string) =>
      api.patch(`/blueprints/${id}/set-visibility`, { visibility }),
    setGlobal: (id: string) => api.patch(`/blueprints/${id}/set-global`),
    uploadIcon: (id: string, formData: FormData) =>
      api.patch(`/blueprints/${id}/icon`, formData),
    getLabels: () => api.get('/labels/blueprints'),
    getLabelValues: (key: string) => api.get(`/labels/blueprints/${key}`),
  },

  deployments: {
    list: (params?: any) => api.get('/deployments', { params }),
    get: (id: string) => api.get(`/deployments/${id}`),
    create: (id: string, data: any) => api.put(`/deployments/${id}`, data),
    update: (id: string, data: any) => api.patch(`/deployments/${id}`, data),
    delete: (id: string) => api.delete(`/deployments/${id}`),
    getOutputs: (id: string) => api.get(`/deployments/${id}/outputs`),
    getCapabilities: (id: string) => api.get(`/deployments/${id}/capabilities`),
  },

  executions: {
    list: (params?: any) => api.get('/executions', { params }),
    get: (id: string) => api.get(`/executions/${id}`),
    start: (data: any) => api.post('/executions', data),
    action: (id: string, action: string) =>
      api.post(`/executions/${id}`, { action }),
  },

  deploymentGroups: {
    list: () => api.get('/deployment-groups'),
    get: (id: string) => api.get(`/deployment-groups/${id}`),
    create: (id: string, data: any) => api.put(`/deployment-groups/${id}`, data),
    update: (id: string, data: any) => api.patch(`/deployment-groups/${id}`, data),
    delete: (id: string) => api.delete(`/deployment-groups/${id}`),
    addDeployments: (id: string, deploymentIds: string[]) =>
      api.post(`/deployment-groups/${id}/add-deployments`, { deployment_ids: deploymentIds }),
    removeDeployments: (id: string, deploymentIds: string[]) =>
      api.post(`/deployment-groups/${id}/remove-deployments`, { deployment_ids: deploymentIds }),
  },

  secrets: {
    list: () => api.get('/secrets'),
    get: (key: string) => api.get(`/secrets/${key}`),
    create: (key: string, data: any) => api.put(`/secrets/${key}`, data),
    update: (key: string, data: any) => api.patch(`/secrets/${key}`, data),
    delete: (key: string) => api.delete(`/secrets/${key}`),
  },

  plugins: {
    list: () => api.get('/plugins'),
    get: (id: string) => api.get(`/plugins/${id}`),
    upload: (id: string, data: any) => api.put(`/plugins/${id}`, data),
    delete: (id: string) => api.delete(`/plugins/${id}`),
  },

  sites: {
    list: () => api.get('/sites'),
    get: (name: string) => api.get(`/sites/${name}`),
    create: (name: string, data: any) => api.put(`/sites/${name}`, data),
    delete: (name: string) => api.delete(`/sites/${name}`),
  },

  agents: {
    list: (params?: any) => api.get('/agents', { params }),
  },

  filters: {
    list: () => api.get('/filters'),
    create: (data: any) => api.post('/filters', data),
    delete: (id: string) => api.delete(`/filters/${id}`),
  },

  users: {
    list: () => api.get('/users'),
    get: (username: string) => api.get(`/users/${username}`),
    create: (data: any) => api.post('/users', data),
    update: (username: string, data: any) => api.patch(`/users/${username}`, data),
    delete: (username: string) => api.delete(`/users/${username}`),
  },

  groups: {
    list: () => api.get('/groups'),
    get: (name: string) => api.get(`/groups/${name}`),
    create: (data: any) => api.post('/groups', data),
    update: (name: string, data: any) => api.patch(`/groups/${name}`, data),
    delete: (name: string) => api.delete(`/groups/${name}`),
  },

  tenants: {
    list: () => api.get('/tenants'),
    create: (data: any) => api.post('/tenants', data),
    delete: (name: string) => api.delete(`/tenants/${name}`),
  },

  events: {
    list: (params?: any) => api.get('/events', { params }),
  },

  snapshots: {
    list: () => api.get('/snapshots'),
    create: () => api.post('/snapshots'),
    delete: (id: string) => api.delete(`/snapshots/${id}`),
  },

  cluster: {
    nodes: () => api.get('/managers'),
    status: () => api.get('/cluster-status'),
  },
};
