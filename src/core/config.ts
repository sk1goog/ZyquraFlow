const defaultBackendUrl = 'http://localhost:8000'

export const config = {
  backendUrl: import.meta.env.VITE_BACKEND_URL ?? defaultBackendUrl,
}
