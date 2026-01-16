import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  DocumentArrowDownIcon,
  EyeIcon,
  TrashIcon,
  DocumentPlusIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline'
import { projectService } from '@/services/projectService'
import { reportService, Report } from '@/services/reportService'
import Button from '@/components/common/Button'
import Modal, { ModalFooter } from '@/components/common/Modal'
import Select from '@/components/common/Select'
import Loading from '@/components/common/Loading'
import Card, { CardHeader } from '@/components/common/Card'
import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableHeaderCell,
  TableCell,
  TableEmpty,
} from '@/components/common/Table'

export default function Reports() {
  const [selectedProject, setSelectedProject] = useState<number | null>(null)
  const [showGenerateModal, setShowGenerateModal] = useState(false)
  const [previewReport, setPreviewReport] = useState<Report | null>(null)
  const queryClient = useQueryClient()

  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectService.list({ page_size: 100 }),
  })

  const { data: reports, isLoading } = useQuery({
    queryKey: ['reports', selectedProject],
    queryFn: () =>
      selectedProject
        ? reportService.list(selectedProject)
        : Promise.resolve({ items: [], total: 0, page: 1, page_size: 10 }),
    enabled: !!selectedProject,
  })

  const generateMutation = useMutation({
    mutationFn: () =>
      reportService.generate(selectedProject!, { report_type: 'tara' }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports', selectedProject] })
      setShowGenerateModal(false)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (reportId: number) =>
      reportService.delete(selectedProject!, reportId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports', selectedProject] })
    },
  })

  const handleDownload = async (report: Report) => {
    try {
      const blob = await reportService.download(selectedProject!, report.id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = report.filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  const getStatusIcon = (status: Report['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'generating':
        return <ClockIcon className="h-5 w-5 text-blue-500 animate-spin" />
      case 'failed':
        return <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
      default:
        return <ClockIcon className="h-5 w-5 text-gray-400" />
    }
  }

  const getStatusLabel = (status: Report['status']) => {
    const labels = {
      pending: '待生成',
      generating: '生成中',
      completed: '已完成',
      failed: '生成失败',
    }
    return labels[status] || status
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">报告中心</h1>
        <p className="mt-1 text-sm text-gray-500">
          生成和管理 TARA 分析报告
        </p>
      </div>

      {/* Project selector */}
      <Card padding="lg">
        <CardHeader
          title="选择项目"
          description="选择一个项目以查看或生成报告"
        />
        <div className="flex items-center gap-4">
          <Select
            value={selectedProject?.toString() || ''}
            onChange={(e) => setSelectedProject(Number(e.target.value) || null)}
            options={[
              { value: '', label: '请选择项目' },
              ...(projects?.items.map((p) => ({
                value: p.id.toString(),
                label: `${p.name}${p.code ? ` (${p.code})` : ''}`,
              })) || []),
            ]}
            className="w-80"
          />
          {selectedProject && (
            <Button
              onClick={() => setShowGenerateModal(true)}
              leftIcon={<DocumentPlusIcon className="h-4 w-4" />}
            >
              生成报告
            </Button>
          )}
        </div>
      </Card>

      {/* Reports list */}
      {selectedProject && (
        <Card padding="none">
          <div className="p-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">报告列表</h3>
          </div>

          {isLoading ? (
            <div className="p-8">
              <Loading text="加载报告列表..." />
            </div>
          ) : (
            <Table>
              <TableHead>
                <TableRow hover={false}>
                  <TableHeaderCell>状态</TableHeaderCell>
                  <TableHeaderCell>报告名称</TableHeaderCell>
                  <TableHeaderCell>类型</TableHeaderCell>
                  <TableHeaderCell>大小</TableHeaderCell>
                  <TableHeaderCell>生成时间</TableHeaderCell>
                  <TableHeaderCell align="right">操作</TableHeaderCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {!reports?.items?.length ? (
                  <TableEmpty colSpan={6} message="暂无报告，点击「生成报告」创建新报告" />
                ) : (
                  reports.items.map((report) => (
                    <TableRow key={report.id}>
                      <TableCell>
                        <div className="flex items-center">
                          {getStatusIcon(report.status)}
                          <span className="ml-2 text-sm">
                            {getStatusLabel(report.status)}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <p className="font-medium text-gray-900">
                          {report.filename}
                        </p>
                      </TableCell>
                      <TableCell>
                        <span className="capitalize">{report.report_type}</span>
                      </TableCell>
                      <TableCell>
                        {report.file_size
                          ? `${(report.file_size / 1024).toFixed(1)} KB`
                          : '-'}
                      </TableCell>
                      <TableCell>
                        {new Date(report.created_at).toLocaleString()}
                      </TableCell>
                      <TableCell align="right">
                        <div className="flex items-center justify-end gap-2">
                          {report.status === 'completed' && (
                            <>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => setPreviewReport(report)}
                                leftIcon={<EyeIcon className="h-4 w-4" />}
                              >
                                预览
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDownload(report)}
                                leftIcon={
                                  <DocumentArrowDownIcon className="h-4 w-4" />
                                }
                              >
                                下载
                              </Button>
                            </>
                          )}
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              if (confirm('确定要删除此报告吗？')) {
                                deleteMutation.mutate(report.id)
                              }
                            }}
                            leftIcon={<TrashIcon className="h-4 w-4 text-red-500" />}
                          />
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </Card>
      )}

      {/* Generate modal */}
      <Modal
        isOpen={showGenerateModal}
        onClose={() => setShowGenerateModal(false)}
        title="生成 TARA 报告"
      >
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            将根据当前项目的资产和威胁分析结果生成符合 ISO 21434 标准的 TARA
            分析报告。
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="text-sm font-medium text-blue-800">报告内容包括：</h4>
            <ul className="mt-2 text-sm text-blue-700 list-disc list-inside space-y-1">
              <li>封面页和文档信息</li>
              <li>术语和定义</li>
              <li>资产清单和安全属性</li>
              <li>威胁场景和攻击路径分析</li>
              <li>风险评估矩阵</li>
              <li>安全需求和缓解措施</li>
            </ul>
          </div>
        </div>

        <ModalFooter>
          <Button
            variant="secondary"
            onClick={() => setShowGenerateModal(false)}
          >
            取消
          </Button>
          <Button
            onClick={() => generateMutation.mutate()}
            loading={generateMutation.isPending}
          >
            生成报告
          </Button>
        </ModalFooter>
      </Modal>

      {/* Preview modal */}
      <Modal
        isOpen={!!previewReport}
        onClose={() => setPreviewReport(null)}
        title={previewReport?.filename || '报告预览'}
        size="full"
      >
        {previewReport && (
          <div className="space-y-4">
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-500">报告类型:</span>
                <span className="ml-2 font-medium capitalize">
                  {previewReport.report_type}
                </span>
              </div>
              <div>
                <span className="text-gray-500">文件大小:</span>
                <span className="ml-2 font-medium">
                  {previewReport.file_size
                    ? `${(previewReport.file_size / 1024).toFixed(1)} KB`
                    : '-'}
                </span>
              </div>
              <div>
                <span className="text-gray-500">生成时间:</span>
                <span className="ml-2 font-medium">
                  {new Date(previewReport.created_at).toLocaleString()}
                </span>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-8 text-center">
              <DocumentArrowDownIcon className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-4 text-gray-600">
                Excel 报告不支持在线预览，请下载后查看
              </p>
              <Button
                className="mt-4"
                onClick={() => handleDownload(previewReport)}
                leftIcon={<DocumentArrowDownIcon className="h-4 w-4" />}
              >
                下载报告
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}
