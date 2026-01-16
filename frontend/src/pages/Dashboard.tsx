import { useQuery } from '@tanstack/react-query'
import {
  FolderIcon,
  CubeIcon,
  ExclamationTriangleIcon,
  ShieldExclamationIcon,
} from '@heroicons/react/24/outline'
import { projectService } from '@/services/projectService'

const statCards = [
  { name: '项目总数', key: 'project_count', icon: FolderIcon, color: 'bg-blue-500' },
  { name: '资产总数', key: 'asset_count', icon: CubeIcon, color: 'bg-green-500' },
  { name: '威胁总数', key: 'threat_count', icon: ExclamationTriangleIcon, color: 'bg-yellow-500' },
  { name: '高风险项', key: 'high_risk_count', icon: ShieldExclamationIcon, color: 'bg-red-500' },
]

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['project-stats'],
    queryFn: () => projectService.getStats(),
  })

  const { data: projects } = useQuery({
    queryKey: ['recent-projects'],
    queryFn: () => projectService.list({ page: 1, page_size: 5 }),
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">仪表盘</h1>
        <p className="mt-1 text-sm text-gray-500">欢迎使用 Intelli-TARA 智能威胁分析与风险评估平台</p>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => (
          <div
            key={card.key}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 ${card.color} rounded-md p-3`}>
                  <card.icon className="h-6 w-6 text-white" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {card.name}
                    </dt>
                    <dd className="text-2xl font-semibold text-gray-900">
                      {isLoading ? '-' : (stats as any)?.[card.key] || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent projects */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">最近项目</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {projects?.items.map((project) => (
            <div key={project.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <FolderIcon className="h-5 w-5 text-gray-400" />
                  <div className="ml-3">
                    <p className="text-sm font-medium text-primary-600 hover:text-primary-700">
                      {project.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {project.code || '未设置编码'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
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
                  <span className="text-sm text-gray-500">
                    {new Date(project.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
          {(!projects?.items || projects.items.length === 0) && (
            <div className="px-4 py-8 text-center text-gray-500">
              暂无项目
            </div>
          )}
        </div>
      </div>

      {/* Quick guide */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">快速指南</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-primary-600">1</div>
            <h3 className="mt-2 font-medium text-gray-900">创建项目</h3>
            <p className="mt-1 text-sm text-gray-500">
              创建新的TARA分析项目，上传架构文档和功能清单
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-primary-600">2</div>
            <h3 className="mt-2 font-medium text-gray-900">AI分析</h3>
            <p className="mt-1 text-sm text-gray-500">
              系统自动识别资产、分析威胁并进行风险评估
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-primary-600">3</div>
            <h3 className="mt-2 font-medium text-gray-900">生成报告</h3>
            <p className="mt-1 text-sm text-gray-500">
              生成符合ISO 21434标准的TARA分析报告
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
