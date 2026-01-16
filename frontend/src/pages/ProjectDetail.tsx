import { useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  ArrowLeftIcon,
  PencilSquareIcon,
  TrashIcon,
  PlayIcon,
  CubeIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  ChartPieIcon,
  ClockIcon,
  UserIcon,
} from '@heroicons/react/24/outline'
import { projectService, ProjectUpdate } from '@/services/projectService'
import { assetService } from '@/services/assetService'
import { threatService } from '@/services/threatService'
import Button from '@/components/common/Button'
import Modal, { ModalFooter } from '@/components/common/Modal'
import Input from '@/components/common/Input'
import Card, { CardHeader } from '@/components/common/Card'
import Loading from '@/components/common/Loading'
import { RiskBadge, StatusBadge } from '@/components/common/Badge'
import { RiskMatrix } from '@/components/business'

export default function ProjectDetail() {
  const { id } = useParams<{ id: string }>()
  const projectId = Number(id)
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const [showEditModal, setShowEditModal] = useState(false)
  const [editData, setEditData] = useState<ProjectUpdate>({})

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectService.get(projectId),
  })

  const { data: assets } = useQuery({
    queryKey: ['assets', projectId],
    queryFn: () => assetService.list(projectId, { page_size: 5 }),
  })

  const { data: threats } = useQuery({
    queryKey: ['threats', projectId],
    queryFn: () => threatService.list(projectId, { page_size: 5 }),
  })

  const { data: riskMatrix } = useQuery({
    queryKey: ['risk-matrix', projectId],
    queryFn: () => threatService.getRiskMatrix(projectId),
  })

  const updateMutation = useMutation({
    mutationFn: (data: ProjectUpdate) => projectService.update(projectId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
      setShowEditModal(false)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: () => projectService.delete(projectId),
    onSuccess: () => {
      navigate('/projects')
    },
  })

  if (isLoading) {
    return <Loading fullScreen text="加载项目详情..." />
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

  const openEditModal = () => {
    setEditData({
      name: project.name,
      code: project.code,
      description: project.description,
    })
    setShowEditModal(true)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/projects"
            className="text-gray-500 hover:text-gray-700 transition-colors"
          >
            <ArrowLeftIcon className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
            <p className="mt-1 text-sm text-gray-500">
              {project.code || '未设置项目编码'}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <Button
            variant="secondary"
            onClick={openEditModal}
            leftIcon={<PencilSquareIcon className="h-4 w-4" />}
          >
            编辑
          </Button>
          <Button
            variant="danger"
            onClick={() => {
              if (confirm('确定要删除此项目吗？此操作不可撤销。')) {
                deleteMutation.mutate()
              }
            }}
            leftIcon={<TrashIcon className="h-4 w-4" />}
          >
            删除
          </Button>
          <Link to={`/projects/${projectId}/analysis`}>
            <Button leftIcon={<PlayIcon className="h-4 w-4" />}>
              开始分析
            </Button>
          </Link>
        </div>
      </div>

      {/* Overview cards */}
      <div className="grid grid-cols-4 gap-4">
        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <DocumentTextIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">文档数量</p>
              <p className="text-2xl font-bold text-gray-900">
                {project.document_count || 0}
              </p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <CubeIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">资产数量</p>
              <p className="text-2xl font-bold text-gray-900">
                {assets?.total || 0}
              </p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-yellow-100 rounded-lg">
              <ExclamationTriangleIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">威胁数量</p>
              <p className="text-2xl font-bold text-gray-900">
                {threats?.total || 0}
              </p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-red-100 rounded-lg">
              <ChartPieIcon className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">高风险项</p>
              <p className="text-2xl font-bold text-red-600">
                {riskMatrix?.high_risk_count || 0}
              </p>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Project info */}
        <Card className="col-span-1">
          <CardHeader title="项目信息" />
          <dl className="space-y-4">
            <div>
              <dt className="text-sm text-gray-500">状态</dt>
              <dd className="mt-1">
                <StatusBadge status={project.status} />
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">描述</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {project.description || '暂无描述'}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500 flex items-center">
                <UserIcon className="h-4 w-4 mr-1" />
                负责人
              </dt>
              <dd className="mt-1 text-sm text-gray-900">
                {project.owner_name || '未指定'}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500 flex items-center">
                <ClockIcon className="h-4 w-4 mr-1" />
                创建时间
              </dt>
              <dd className="mt-1 text-sm text-gray-900">
                {new Date(project.created_at).toLocaleString()}
              </dd>
            </div>
            {project.updated_at && (
              <div>
                <dt className="text-sm text-gray-500">更新时间</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {new Date(project.updated_at).toLocaleString()}
                </dd>
              </div>
            )}
          </dl>
        </Card>

        {/* Risk Matrix */}
        <Card className="col-span-2">
          <CardHeader title="风险矩阵" />
          <RiskMatrix data={riskMatrix} />
        </Card>
      </div>

      {/* Recent assets and threats */}
      <div className="grid grid-cols-2 gap-6">
        {/* Recent assets */}
        <Card>
          <CardHeader
            title="最近资产"
            actions={
              <Link
                to={`/projects/${projectId}/analysis`}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                查看全部
              </Link>
            }
          />
          {assets?.items?.length ? (
            <div className="space-y-3">
              {assets.items.map((asset) => (
                <div
                  key={asset.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center">
                    <CubeIcon className="h-5 w-5 text-gray-400 mr-3" />
                    <div>
                      <p className="font-medium text-gray-900">{asset.name}</p>
                      <p className="text-xs text-gray-500">
                        {asset.asset_id} • {asset.category}
                      </p>
                    </div>
                  </div>
                  <StatusBadge
                    status={asset.is_confirmed ? 'confirmed' : 'pending'}
                  />
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center py-8 text-gray-500">暂无资产数据</p>
          )}
        </Card>

        {/* Recent threats */}
        <Card>
          <CardHeader
            title="最近威胁"
            actions={
              <Link
                to={`/projects/${projectId}/analysis`}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                查看全部
              </Link>
            }
          />
          {threats?.items?.length ? (
            <div className="space-y-3">
              {threats.items.map((threat) => (
                <div
                  key={threat.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center">
                    <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500 mr-3" />
                    <div>
                      <p className="font-medium text-gray-900 truncate max-w-xs">
                        {threat.threat_description}
                      </p>
                      <p className="text-xs text-gray-500">
                        {threat.threat_id} • {threat.stride_type}
                      </p>
                    </div>
                  </div>
                  <RiskBadge level={threat.risk_level || 0} />
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center py-8 text-gray-500">暂无威胁数据</p>
          )}
        </Card>
      </div>

      {/* Edit modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        title="编辑项目"
      >
        <div className="space-y-4">
          <Input
            label="项目名称"
            value={editData.name || ''}
            onChange={(e) => setEditData({ ...editData, name: e.target.value })}
          />
          <Input
            label="项目编码"
            value={editData.code || ''}
            onChange={(e) => setEditData({ ...editData, code: e.target.value })}
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              项目描述
            </label>
            <textarea
              value={editData.description || ''}
              onChange={(e) =>
                setEditData({ ...editData, description: e.target.value })
              }
              rows={3}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            />
          </div>
        </div>

        <ModalFooter>
          <Button variant="secondary" onClick={() => setShowEditModal(false)}>
            取消
          </Button>
          <Button
            onClick={() => updateMutation.mutate(editData)}
            loading={updateMutation.isPending}
          >
            保存
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  )
}
