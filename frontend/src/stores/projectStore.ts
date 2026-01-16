import { create } from 'zustand'

interface Project {
  id: number
  name: string
  code?: string
  description?: string
  status: string
  owner_id: number
  owner_name?: string
  created_at: string
  updated_at?: string
}

interface ProjectState {
  currentProject: Project | null
  setCurrentProject: (project: Project | null) => void
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: null,
  setCurrentProject: (project) => set({ currentProject: project }),
}))
