import api from './api'

export interface Report {
  id: number
  project_id: number
  version_id?: number
  report_type: string
  filename: string
  file_path?: string
  file_size?: number
  status: 'pending' | 'generating' | 'completed' | 'failed'
  config?: any
  created_by: number
  created_at: string
  updated_at?: string
}

export interface ReportCreate {
  report_type: string
  config?: any
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export const reportService = {
  list: async (
    projectId: number,
    params?: {
      page?: number
      page_size?: number
      report_type?: string
    }
  ): Promise<PaginatedResponse<Report>> => {
    const response = await api.get(`/projects/${projectId}/reports`, { params })
    return response.data
  },

  get: async (projectId: number, reportId: number): Promise<Report> => {
    const response = await api.get(`/projects/${projectId}/reports/${reportId}`)
    return response.data
  },

  generate: async (projectId: number, data?: ReportCreate): Promise<Report> => {
    const response = await api.post(`/projects/${projectId}/reports/generate`, data || {})
    return response.data
  },

  delete: async (projectId: number, reportId: number): Promise<void> => {
    await api.delete(`/projects/${projectId}/reports/${reportId}`)
  },

  download: async (projectId: number, reportId: number): Promise<Blob> => {
    const response = await api.get(`/projects/${projectId}/reports/${reportId}/download`, {
      responseType: 'blob',
    })
    return response.data
  },

  preview: async (projectId: number, reportId: number): Promise<any> => {
    const response = await api.get(`/projects/${projectId}/reports/${reportId}/preview`)
    return response.data
  },
}
