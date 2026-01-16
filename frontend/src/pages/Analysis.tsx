import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'

const tabs = [
  { key: 'documents', label: '文档管理' },
  { key: 'assets', label: '资产识别' },
  { key: 'threats', label: '威胁分析' },
  { key: 'graph', label: '知识图谱' },
]

export default function Analysis() {
  const { id } = useParams<{ id: string }>()
  const projectId = Number(id)
  const [activeTab, setActiveTab] = useState('documents')

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link to={`/projects/${projectId}`} className="text-gray-500 hover:text-gray-700">
          <ArrowLeftIcon className="h-5 w-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">TARA 分析工作台</h1>
          <p className="mt-1 text-sm text-gray-500">执行威胁分析与风险评估</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.key
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab content */}
      <div className="bg-white shadow rounded-lg p-6">
        {activeTab === 'documents' && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">文档管理</h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
              <p className="text-gray-500">拖拽文件到此处或点击上传</p>
              <p className="mt-2 text-sm text-gray-400">
                支持 PDF, Word, Excel, PPT, 图片等格式
              </p>
              <button className="mt-4 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700">
                选择文件
              </button>
            </div>
          </div>
        )}

        {activeTab === 'assets' && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">资产列表</h3>
              <div className="space-x-2">
                <button className="px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                  导入资产
                </button>
                <button className="px-3 py-1.5 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700">
                  AI 识别
                </button>
              </div>
            </div>
            <div className="text-center py-12 text-gray-500">
              暂无资产数据，请先上传文档并执行 AI 识别
            </div>
          </div>
        )}

        {activeTab === 'threats' && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">威胁分析</h3>
              <div className="space-x-2">
                <button className="px-3 py-1.5 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700">
                  AI 分析
                </button>
              </div>
            </div>
            <div className="text-center py-12 text-gray-500">
              暂无威胁数据，请先完成资产识别后执行威胁分析
            </div>
          </div>
        )}

        {activeTab === 'graph' && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">知识图谱</h3>
            <div className="h-96 border border-gray-200 rounded-lg flex items-center justify-center text-gray-500">
              资产关系图谱将在此显示
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
