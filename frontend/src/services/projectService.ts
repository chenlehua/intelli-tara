import api from './api'

export interface Project {
  id: number
  name: string
  code?: string
  description?: string
  status: string
  owner_id: number
  owner_name?: string
  created_at: string
  updated_at?: string
  asset_count?: number
  threat_count?: number
  report_count?: number
}

export interface ProjectCreate {
  name: string
  code?: string
  description?: string
}

export interface ProjectUpdate {
  name?: string
  code?: string
  description?: string
  status?: string
}

export interface ProjectStats {
  project_count: number
  asset_count: number
  threat_count: number
  high_risk_count: number
  risk_distribution?: Record<string, number>
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export const projectService = {
  list: async (params?: {
    page?: number
    page_size?: number
    status?: string
    search?: string
  }): Promise<PaginatedResponse<Project>> => {
    const response = await api.get('/projects', { params })
    return response.data
  },

  get: async (id: number): Promise<Project> => {
    const response = await api.get(`/projects/${id}`)
    return response.data
  },

  create: async (data: ProjectCreate): Promise<Project> => {
    const response = await api.post('/projects', data)
    return response.data
  },

  update: async (id: number, data: ProjectUpdate): Promise<Project> => {
    const response = await api.put(`/projects/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/projects/${id}`)
  },

  getStats: async (): Promise<ProjectStats> => {
    const response = await api.get('/projects/stats')
    return response.data
  },

  getVersions: async (id: number) => {
    const response = await api.get(`/projects/${id}/versions`)
    return response.data
  },

  createVersion: async (id: number, data: { version: string; description?: string }) => {
    const response = await api.post(`/projects/${id}/versions`, data)
    return response.data
  },

  getMembers: async (id: number) => {
    const response = await api.get(`/projects/${id}/members`)
    return response.data
  },

  addMember: async (id: number, data: { user_id: number; role: string }) => {
    const response = await api.post(`/projects/${id}/members`, data)
    return response.data
  },
}
