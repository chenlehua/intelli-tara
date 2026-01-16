import api from './api'

export interface WP29Threat {
  id: number
  code: string
  category: string
  subcategory?: string
  threat_description_en: string
  threat_description_zh?: string
  mitigation_en?: string
  mitigation_zh?: string
}

export interface AttackPattern {
  id: number
  pattern_id: string
  name: string
  description?: string
  prerequisites?: string
  attack_steps?: string
  mitigations?: string
  related_cwe?: string[]
  related_capec?: string
}

export interface SecurityRequirement {
  id: number
  requirement_id: string
  category: string
  requirement_text: string
  description?: string
  source?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export const knowledgeService = {
  // WP29 Threats
  listWP29Threats: async (params?: {
    page?: number
    page_size?: number
    category?: string
    search?: string
  }): Promise<PaginatedResponse<WP29Threat>> => {
    const response = await api.get('/knowledge/wp29-threats', { params })
    return response.data
  },

  getWP29Threat: async (id: number): Promise<WP29Threat> => {
    const response = await api.get(`/knowledge/wp29-threats/${id}`)
    return response.data
  },

  // Attack Patterns
  listAttackPatterns: async (params?: {
    page?: number
    page_size?: number
    search?: string
  }): Promise<PaginatedResponse<AttackPattern>> => {
    const response = await api.get('/knowledge/attack-patterns', { params })
    return response.data
  },

  getAttackPattern: async (id: number): Promise<AttackPattern> => {
    const response = await api.get(`/knowledge/attack-patterns/${id}`)
    return response.data
  },

  // Security Requirements
  listSecurityRequirements: async (params?: {
    page?: number
    page_size?: number
    category?: string
    search?: string
  }): Promise<PaginatedResponse<SecurityRequirement>> => {
    const response = await api.get('/knowledge/security-requirements', { params })
    return response.data
  },

  // Search
  search: async (query: string): Promise<{
    wp29_threats: WP29Threat[]
    attack_patterns: AttackPattern[]
    security_requirements: SecurityRequirement[]
  }> => {
    const response = await api.get('/knowledge/search', { params: { query } })
    return response.data
  },

  // Get mitigation suggestions
  getMitigationSuggestions: async (threatDescription: string): Promise<{
    wp29_mitigations: string[]
    security_requirements: SecurityRequirement[]
  }> => {
    const response = await api.post('/knowledge/mitigation-suggestions', {
      threat_description: threatDescription,
    })
    return response.data
  },
}
