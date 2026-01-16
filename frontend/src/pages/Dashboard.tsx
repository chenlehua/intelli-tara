import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
  FolderIcon,
  CubeIcon,
  ExclamationTriangleIcon,
  ShieldExclamationIcon,
  ArrowRightIcon,
  PlusIcon,
} from '@heroicons/react/24/outline'
import { projectService } from '@/services/projectService'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import Loading from '@/components/common/Loading'
import { StatusBadge, RiskBadge } from '@/components/common/Badge'

const statCards = [
  {
    name: '项目总数',
    key: 'project_count',
    icon: FolderIcon,
    color: 'bg-blue-500',
    bgColor: 'bg-blue-100',
  },
  {
    name: '资产总数',
    key: 'asset_count',
    icon: CubeIcon,
    color: 'bg-green-500',
    bgColor: 'bg-green-100',
  },
  {
    name: '威胁总数',
    key: 'threat_count',
    icon: ExclamationTriangleIcon,
    color: 'bg-yellow-500',
    bgColor: 'bg-yellow-100',
  },
  {
    name: '高风险项',
    key: 'high_risk_count',
    icon: ShieldExclamationIcon,
    color: 'bg-red-500',
    bgColor: 'bg-red-100',
  },
]

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['project-stats'],
    queryFn: () => projectService.getStats(),
  })

  const { data: projects, isLoading: projectsLoading } = useQuery({
    queryKey: ['recent-projects'],
    queryFn: () => projectService.list({ page: 1, page_size: 5 }),
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">仪表盘</h1>
          <p className="mt-1 text-sm text-gray-500">
            欢迎使用 Intelli-TARA 智能威胁分析与风险评估平台
          </p>
        </div>
        <Link to="/projects">
          <Button leftIcon={<PlusIcon className="h-4 w-4" />}>新建项目</Button>
        </Link>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => (
          <Card key={card.key} hover>
            <div className="flex items-center">
              <div className={`flex-shrink-0 ${card.bgColor} rounded-lg p-3`}>
                <card.icon className={`h-6 w-6 ${card.color.replace('bg-', 'text-')}`} />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {card.name}
                  </dt>
                  <dd className="text-2xl font-bold text-gray-900">
                    {statsLoading ? (
                      <span className="animate-pulse">-</span>
                    ) : (
                      (stats as any)?.[card.key] || 0
                    )}
                  </dd>
                </dl>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent projects */}
        <Card padding="none">
          <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-lg font-medium text-gray-900">最近项目</h2>
            <Link
              to="/projects"
              className="text-sm text-primary-600 hover:text-primary-700 flex items-center"
            >
              查看全部
              <ArrowRightIcon className="h-4 w-4 ml-1" />
            </Link>
          </div>
          <div className="divide-y divide-gray-200">
            {projectsLoading ? (
              <div className="p-8">
                <Loading text="加载中..." />
              </div>
            ) : projects?.items.length === 0 ? (
              <div className="px-6 py-8 text-center text-gray-500">
                <FolderIcon className="mx-auto h-12 w-12 text-gray-300" />
                <p className="mt-2">暂无项目</p>
                <Link to="/projects" className="mt-4 inline-block">
                  <Button size="sm" variant="secondary">
                    创建第一个项目
                  </Button>
                </Link>
              </div>
            ) : (
              projects?.items.map((project) => (
                <Link
                  key={project.id}
                  to={`/projects/${project.id}`}
                  className="block px-6 py-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center min-w-0">
                      <FolderIcon className="h-5 w-5 text-gray-400 flex-shrink-0" />
                      <div className="ml-3 min-w-0">
                        <p className="text-sm font-medium text-primary-600 truncate">
                          {project.name}
                        </p>
                        <p className="text-xs text-gray-500">
                          {project.code || '未设置编码'}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4 ml-4">
                      <StatusBadge status={project.status} />
                      <span className="text-sm text-gray-500 hidden sm:block">
                        {new Date(project.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </Link>
              ))
            )}
          </div>
        </Card>

        {/* Quick guide */}
        <Card>
          <h2 className="text-lg font-medium text-gray-900 mb-4">快速指南</h2>
          <div className="space-y-4">
            <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-lg font-bold text-primary-600">1</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">创建项目</h3>
                <p className="mt-1 text-sm text-gray-500">
                  创建新的 TARA 分析项目，配置项目基本信息和分析范围
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-lg font-bold text-primary-600">2</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">上传文档</h3>
                <p className="mt-1 text-sm text-gray-500">
                  上传系统架构文档、功能规格书、通信矩阵等技术文档
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-lg font-bold text-primary-600">3</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">AI 分析</h3>
                <p className="mt-1 text-sm text-gray-500">
                  系统自动识别资产、分析威胁场景并进行风险评估
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0 w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-lg font-bold text-primary-600">4</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">生成报告</h3>
                <p className="mt-1 text-sm text-gray-500">
                  生成符合 ISO 21434 标准的 TARA 分析报告
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Risk distribution */}
      {stats?.risk_distribution && (
        <Card>
          <h2 className="text-lg font-medium text-gray-900 mb-4">风险分布概览</h2>
          <div className="grid grid-cols-5 gap-4">
            {[
              { level: 5, label: '严重' },
              { level: 4, label: '高' },
              { level: 3, label: '中' },
              { level: 2, label: '低' },
              { level: 1, label: '可接受' },
            ].map(({ level, label }) => {
              const count = stats.risk_distribution?.[level] || 0
              return (
                <div key={level} className="text-center">
                  <div className="flex items-center justify-center mb-2">
                    <RiskBadge level={level} />
                  </div>
                  <p className="text-2xl font-bold text-gray-900">{count}</p>
                  <p className="text-sm text-gray-500">{label}</p>
                </div>
              )
            })}
          </div>
        </Card>
      )}
    </div>
  )
}
