import api from './api'

export interface Threat {
  id: number
  project_id: number
  version_id?: number
  asset_id: number
  asset_name?: string
  threat_id: string
  security_attribute: string
  stride_type: string
  threat_description: string
  damage_scenario?: string
  attack_path?: string
  source_reference?: string
  wp29_mapping?: string
  attack_vector?: string
  attack_complexity?: string
  privileges_required?: string
  user_interaction?: string
  attack_feasibility?: string
  attack_feasibility_value?: number
  impact_safety?: string
  impact_financial?: string
  impact_operational?: string
  impact_privacy?: string
  impact_level?: string
  impact_level_value?: number
  risk_level?: number
  risk_level_label?: string
  treatment_decision?: string
  is_ai_generated: boolean
  is_confirmed: boolean
  created_at: string
  updated_at?: string
  mitigations: Mitigation[]
}

export interface Mitigation {
  id: number
  threat_id: number
  security_goal?: string
  security_requirement?: string
  wp29_control_mapping?: string
  implementation_status: string
  created_at: string
  updated_at?: string
}

export interface ThreatCreate {
  asset_id: number
  threat_id: string
  security_attribute: string
  stride_type: string
  threat_description: string
  damage_scenario?: string
  attack_path?: string
  source_reference?: string
  wp29_mapping?: string
  attack_vector?: string
  attack_complexity?: string
  privileges_required?: string
  user_interaction?: string
  impact_safety?: string
  impact_financial?: string
  impact_operational?: string
  impact_privacy?: string
}

export interface ThreatUpdate {
  threat_id?: string
  security_attribute?: string
  stride_type?: string
  threat_description?: string
  damage_scenario?: string
  attack_path?: string
  source_reference?: string
  wp29_mapping?: string
  attack_vector?: string
  attack_complexity?: string
  privileges_required?: string
  user_interaction?: string
  impact_safety?: string
  impact_financial?: string
  impact_operational?: string
  impact_privacy?: string
  treatment_decision?: string
  is_confirmed?: boolean
}

export interface RiskMatrix {
  matrix: number[][]
  threat_counts: Record<number, number>
  total_threats: number
  high_risk_count: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export const threatService = {
  list: async (
    projectId: number,
    params?: {
      page?: number
      page_size?: number
      asset_id?: number
      stride_type?: string
      risk_level?: number
      confirmed?: boolean
    }
  ): Promise<PaginatedResponse<Threat>> => {
    const response = await api.get(`/projects/${projectId}/threats`, { params })
    return response.data
  },

  get: async (projectId: number, threatId: number): Promise<Threat> => {
    const response = await api.get(`/projects/${projectId}/threats/${threatId}`)
    return response.data
  },

  create: async (projectId: number, data: ThreatCreate): Promise<Threat> => {
    const response = await api.post(`/projects/${projectId}/threats`, data)
    return response.data
  },

  update: async (projectId: number, threatId: number, data: ThreatUpdate): Promise<Threat> => {
    const response = await api.put(`/projects/${projectId}/threats/${threatId}`, data)
    return response.data
  },

  delete: async (projectId: number, threatId: number): Promise<void> => {
    await api.delete(`/projects/${projectId}/threats/${threatId}`)
  },

  addMitigation: async (
    projectId: number,
    threatId: number,
    data: {
      security_goal?: string
      security_requirement?: string
      wp29_control_mapping?: string
      implementation_status?: string
    }
  ): Promise<Mitigation> => {
    const response = await api.post(`/projects/${projectId}/threats/${threatId}/mitigations`, data)
    return response.data
  },

  getRiskMatrix: async (projectId: number): Promise<RiskMatrix> => {
    const response = await api.get(`/projects/${projectId}/threats/risk-matrix`)
    return response.data
  },

  analyze: async (projectId: number, assetId?: number): Promise<{ task_id: string }> => {
    const response = await api.post(`/projects/${projectId}/threats/analyze`, {}, {
      params: assetId ? { asset_id: assetId } : undefined,
    })
    return response.data
  },
}
