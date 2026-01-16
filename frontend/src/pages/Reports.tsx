import { DocumentChartBarIcon } from '@heroicons/react/24/outline'

export default function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">报告中心</h1>
        <p className="mt-1 text-sm text-gray-500">查看和管理TARA分析报告</p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="p-8 text-center">
          <DocumentChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">暂无报告</h3>
          <p className="mt-1 text-sm text-gray-500">
            完成TARA分析后可在此生成和管理报告
          </p>
        </div>
      </div>
    </div>
  )
}
