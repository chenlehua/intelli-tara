import api from './api'

export interface Document {
  id: number
  project_id: number
  filename: string
  file_type: string
  file_size: number
  file_path?: string
  category?: string
  description?: string
  parse_status: 'pending' | 'parsing' | 'completed' | 'failed'
  parse_result?: any
  created_at: string
  updated_at?: string
}

export interface DocumentCreate {
  category?: string
  description?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export const documentService = {
  list: async (
    projectId: number,
    params?: {
      page?: number
      page_size?: number
      category?: string
    }
  ): Promise<PaginatedResponse<Document>> => {
    const response = await api.get(`/projects/${projectId}/documents`, { params })
    return response.data
  },

  get: async (projectId: number, docId: number): Promise<Document> => {
    const response = await api.get(`/projects/${projectId}/documents/${docId}`)
    return response.data
  },

  upload: async (
    projectId: number,
    files: FileList,
    metadata?: DocumentCreate
  ): Promise<Document[]> => {
    const formData = new FormData()
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i])
    }
    if (metadata?.category) {
      formData.append('category', metadata.category)
    }
    if (metadata?.description) {
      formData.append('description', metadata.description)
    }

    const response = await api.post(`/projects/${projectId}/documents/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  delete: async (projectId: number, docId: number): Promise<void> => {
    await api.delete(`/projects/${projectId}/documents/${docId}`)
  },

  parse: async (projectId: number, docId: number): Promise<{ task_id: string }> => {
    const response = await api.post(`/projects/${projectId}/documents/${docId}/parse`)
    return response.data
  },

  getParseResult: async (projectId: number, docId: number): Promise<any> => {
    const response = await api.get(`/projects/${projectId}/documents/${docId}/parse-result`)
    return response.data
  },

  download: async (projectId: number, docId: number): Promise<Blob> => {
    const response = await api.get(`/projects/${projectId}/documents/${docId}/download`, {
      responseType: 'blob',
    })
    return response.data
  },
}
