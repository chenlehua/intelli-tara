import { useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
  ArrowLeftIcon,
  DocumentTextIcon,
  CubeIcon,
  ExclamationTriangleIcon,
  ShareIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline'
import { projectService } from '@/services/projectService'
import Tabs from '@/components/common/Tabs'
import Loading from '@/components/common/Loading'
import Card from '@/components/common/Card'
import {
  DocumentUploader,
  AssetList,
  ThreatTable,
  GraphViewer,
  RiskMatrix,
} from '@/components/business'

const tabs = [
  { key: 'documents', label: '文档管理', icon: <DocumentTextIcon className="h-4 w-4" /> },
  { key: 'assets', label: '资产识别', icon: <CubeIcon className="h-4 w-4" /> },
  { key: 'threats', label: '威胁分析', icon: <ExclamationTriangleIcon className="h-4 w-4" /> },
  { key: 'graph', label: '知识图谱', icon: <ShareIcon className="h-4 w-4" /> },
  { key: 'matrix', label: '风险矩阵', icon: <ChartBarIcon className="h-4 w-4" /> },
]

export default function Analysis() {
  const { id } = useParams<{ id: string }>()
  const projectId = Number(id)
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('documents')

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectService.get(projectId),
  })

  if (isLoading) {
    return <Loading fullScreen text="加载项目信息..." />
  }

  if (!project) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">项目不存在</p>
        <button
          onClick={() => navigate('/projects')}
          className="mt-4 text-primary-600 hover:text-primary-700"
        >
          返回项目列表
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to={`/projects/${projectId}`}
            className="text-gray-500 hover:text-gray-700 transition-colors"
          >
            <ArrowLeftIcon className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">TARA 分析工作台</h1>
            <p className="mt-1 text-sm text-gray-500">
              {project.name} {project.code && `(${project.code})`}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
              project.status === 'completed'
                ? 'bg-green-100 text-green-800'
                : project.status === 'analyzing'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {project.status === 'draft'
              ? '草稿'
              : project.status === 'analyzing'
              ? '分析中'
              : project.status === 'completed'
              ? '已完成'
              : project.status}
          </span>
        </div>
      </div>

      {/* Progress indicator */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <ProgressStep
              number={1}
              label="上传文档"
              active={activeTab === 'documents'}
              completed={true}
            />
            <ProgressStep
              number={2}
              label="识别资产"
              active={activeTab === 'assets'}
              completed={false}
            />
            <ProgressStep
              number={3}
              label="威胁分析"
              active={activeTab === 'threats'}
              completed={false}
            />
            <ProgressStep
              number={4}
              label="风险评估"
              active={activeTab === 'matrix'}
              completed={false}
            />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

      {/* Tab content */}
      <Card padding="lg">
        {activeTab === 'documents' && (
          <DocumentUploader projectId={projectId} />
        )}

        {activeTab === 'assets' && (
          <AssetList projectId={projectId} />
        )}

        {activeTab === 'threats' && (
          <ThreatTable projectId={projectId} />
        )}

        {activeTab === 'graph' && (
          <GraphViewer projectId={projectId} />
        )}

        {activeTab === 'matrix' && (
          <RiskMatrix projectId={projectId} />
        )}
      </Card>
    </div>
  )
}

interface ProgressStepProps {
  number: number
  label: string
  active: boolean
  completed: boolean
}

function ProgressStep({ number, label, active, completed }: ProgressStepProps) {
  return (
    <div className="flex items-center">
      <div
        className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium ${
          active
            ? 'bg-primary-600 text-white'
            : completed
            ? 'bg-green-500 text-white'
            : 'bg-gray-200 text-gray-600'
        }`}
      >
        {completed && !active ? '✓' : number}
      </div>
      <span
        className={`ml-2 text-sm ${
          active ? 'text-primary-600 font-medium' : 'text-gray-500'
        }`}
      >
        {label}
      </span>
    </div>
  )
}
