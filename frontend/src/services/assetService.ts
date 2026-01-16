import api from './api'

export interface Asset {
  id: number
  project_id: number
  version_id?: number
  asset_id: string
  name: string
  category: string
  subcategory?: string
  description?: string
  remarks?: string
  authenticity: boolean
  integrity: boolean
  non_repudiation: boolean
  confidentiality: boolean
  availability: boolean
  authorization: boolean
  is_ai_generated: boolean
  is_confirmed: boolean
  created_at: string
  updated_at?: string
}

export interface AssetCreate {
  asset_id: string
  name: string
  category: string
  subcategory?: string
  description?: string
  remarks?: string
  authenticity?: boolean
  integrity?: boolean
  non_repudiation?: boolean
  confidentiality?: boolean
  availability?: boolean
  authorization?: boolean
}

export interface AssetUpdate {
  asset_id?: string
  name?: string
  category?: string
  subcategory?: string
  description?: string
  remarks?: string
  authenticity?: boolean
  integrity?: boolean
  non_repudiation?: boolean
  confidentiality?: boolean
  availability?: boolean
  authorization?: boolean
  is_confirmed?: boolean
}

export interface AssetGraph {
  nodes: Array<{
    id: string
    name: string
    category: string
    subcategory?: string
  }>
  edges: Array<{
    source: string
    target: string
    type: string
    protocol?: string
  }>
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export const assetService = {
  list: async (
    projectId: number,
    params?: {
      page?: number
      page_size?: number
      category?: string
      confirmed?: boolean
    }
  ): Promise<PaginatedResponse<Asset>> => {
    const response = await api.get(`/projects/${projectId}/assets`, { params })
    return response.data
  },

  get: async (projectId: number, assetId: number): Promise<Asset> => {
    const response = await api.get(`/projects/${projectId}/assets/${assetId}`)
    return response.data
  },

  create: async (projectId: number, data: AssetCreate): Promise<Asset> => {
    const response = await api.post(`/projects/${projectId}/assets`, data)
    return response.data
  },

  update: async (projectId: number, assetId: number, data: AssetUpdate): Promise<Asset> => {
    const response = await api.put(`/projects/${projectId}/assets/${assetId}`, data)
    return response.data
  },

  delete: async (projectId: number, assetId: number): Promise<void> => {
    await api.delete(`/projects/${projectId}/assets/${assetId}`)
  },

  confirm: async (projectId: number, assetId: number): Promise<void> => {
    await api.post(`/projects/${projectId}/assets/${assetId}/confirm`)
  },

  getGraph: async (projectId: number): Promise<AssetGraph> => {
    const response = await api.get(`/projects/${projectId}/assets/graph`)
    return response.data
  },

  identify: async (projectId: number, documentId?: number): Promise<{ task_id: string }> => {
    const response = await api.post(`/projects/${projectId}/assets/identify`, {}, {
      params: documentId ? { document_id: documentId } : undefined,
    })
    return response.data
  },
}
