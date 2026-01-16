import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
  DocumentTextIcon,
  CubeIcon,
  ExclamationTriangleIcon,
  DocumentChartBarIcon,
  ArrowLeftIcon,
} from '@heroicons/react/24/outline'
import { projectService } from '@/services/projectService'

export default function ProjectDetail() {
  const { id } = useParams<{ id: string }>()
  const projectId = Number(id)

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectService.get(projectId),
    enabled: !!projectId,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">加载中...</div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">项目不存在</div>
      </div>
    )
  }

  const stats = [
    { name: '资产数量', value: project.asset_count || 0, icon: CubeIcon },
    { name: '威胁数量', value: project.threat_count || 0, icon: ExclamationTriangleIcon },
    { name: '报告数量', value: project.report_count || 0, icon: DocumentChartBarIcon },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link
          to="/projects"
          className="text-gray-500 hover:text-gray-700"
        >
          <ArrowLeftIcon className="h-5 w-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
          <p className="mt-1 text-sm text-gray-500">
            {project.code || '未设置编码'} | {project.owner_name || '未知负责人'}
          </p>
        </div>
      </div>

      {/* Project info */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">项目信息</h2>
        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">项目名称</dt>
            <dd className="mt-1 text-sm text-gray-900">{project.name}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">项目编码</dt>
            <dd className="mt-1 text-sm text-gray-900">{project.code || '-'}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">状态</dt>
            <dd className="mt-1">
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
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
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">创建时间</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {new Date(project.created_at).toLocaleString()}
            </dd>
          </div>
          <div className="sm:col-span-2">
            <dt className="text-sm font-medium text-gray-500">项目描述</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {project.description || '暂无描述'}
            </dd>
          </div>
        </dl>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="text-lg font-semibold text-gray-900">{stat.value}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">快速操作</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Link
            to={`/projects/${projectId}/analysis`}
            className="flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
          >
            <DocumentTextIcon className="h-5 w-5 mr-2" />
            开始分析
          </Link>
          <button className="flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            <CubeIcon className="h-5 w-5 mr-2" />
            管理资产
          </button>
          <button className="flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            <DocumentChartBarIcon className="h-5 w-5 mr-2" />
            生成报告
          </button>
        </div>
      </div>
    </div>
  )
}
