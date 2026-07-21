import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v3.1';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
    'Tenant': 'default_tenant',
  },
});

const AUTH_STORAGE_KEY = 'windriver_auth';

export function setAuth(username: string, password: string) {
  const encoded = btoa(`${username}:${password}`);
  const authHeader = `Basic ${encoded}`;
  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify({ username, password, authHeader }));
  api.defaults.headers.common['Authorization'] = authHeader;
}

export function getAuth(): { username: string; password: string } | null {
  try {
    const stored = localStorage.getItem(AUTH_STORAGE_KEY);
    if (stored) return JSON.parse(stored);
  } catch {}
  return null;
}

export function clearAuth() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  delete api.defaults.headers.common['Authorization'];
}

export function isAuthenticated(): boolean {
  return !!api.defaults.headers.common['Authorization'];
}

const authInterceptor = api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuth();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

export { API_BASE };
