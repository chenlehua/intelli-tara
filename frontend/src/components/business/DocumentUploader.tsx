import { useState, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  DocumentIcon,
  ArrowUpTrayIcon,
  TrashIcon,
  EyeIcon,
  CloudArrowUpIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline'
import { clsx } from 'clsx'
import { documentService, Document } from '@/services/documentService'
import Button from '@/components/common/Button'
import Modal from '@/components/common/Modal'
import Loading from '@/components/common/Loading'
import { StatusBadge } from '@/components/common/Badge'

interface DocumentUploaderProps {
  projectId: number
}

export default function DocumentUploader({ projectId }: DocumentUploaderProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null)
  const queryClient = useQueryClient()

  const { data: documents, isLoading } = useQuery({
    queryKey: ['documents', projectId],
    queryFn: () => documentService.list(projectId),
  })

  const uploadMutation = useMutation({
    mutationFn: (files: FileList) => documentService.upload(projectId, files),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents', projectId] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (docId: number) => documentService.delete(projectId, docId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents', projectId] })
    },
  })

  const parseMutation = useMutation({
    mutationFn: (docId: number) => documentService.parse(projectId, docId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents', projectId] })
    },
  })

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragging(false)
      if (e.dataTransfer.files.length > 0) {
        uploadMutation.mutate(e.dataTransfer.files)
      }
    },
    [uploadMutation]
  )

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      uploadMutation.mutate(e.target.files)
    }
  }

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase()
    const iconColors: Record<string, string> = {
      pdf: 'text-red-500',
      doc: 'text-blue-500',
      docx: 'text-blue-500',
      xls: 'text-green-500',
      xlsx: 'text-green-500',
      ppt: 'text-orange-500',
      pptx: 'text-orange-500',
      png: 'text-purple-500',
      jpg: 'text-purple-500',
      jpeg: 'text-purple-500',
    }
    return iconColors[ext || ''] || 'text-gray-500'
  }

  const getParseStatus = (doc: Document) => {
    if (doc.parse_status === 'completed') {
      return (
        <span className="flex items-center text-green-600 text-sm">
          <CheckCircleIcon className="h-4 w-4 mr-1" />
          解析完成
        </span>
      )
    }
    if (doc.parse_status === 'failed') {
      return (
        <span className="flex items-center text-red-600 text-sm">
          <ExclamationCircleIcon className="h-4 w-4 mr-1" />
          解析失败
        </span>
      )
    }
    if (doc.parse_status === 'parsing') {
      return (
        <span className="flex items-center text-blue-600 text-sm">
          <Loading size="sm" className="mr-1" />
          解析中
        </span>
      )
    }
    return <StatusBadge status="pending" />
  }

  return (
    <div className="space-y-6">
      {/* Upload area */}
      <div
        className={clsx(
          'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
          isDragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
        )}
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-4 text-gray-600">
          拖拽文件到此处或点击上传
        </p>
        <p className="mt-2 text-sm text-gray-400">
          支持 PDF, Word, Excel, PPT, 图片等格式
        </p>
        <label className="mt-4 inline-block cursor-pointer">
          <input
            type="file"
            multiple
            onChange={handleFileSelect}
            className="hidden"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.png,.jpg,.jpeg,.gif"
          />
          <span className="inline-flex items-center justify-center font-medium rounded-md px-4 py-2 text-sm bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            {uploadMutation.isPending ? (
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            ) : (
              <ArrowUpTrayIcon className="h-4 w-4 mr-2" />
            )}
            选择文件
          </span>
        </label>
      </div>

      {/* Document list */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          已上传文档 ({documents?.items?.length || 0})
        </h3>

        {isLoading ? (
          <Loading text="加载中..." />
        ) : !documents?.items?.length ? (
          <div className="text-center py-8 text-gray-500">
            暂无文档，请先上传
          </div>
        ) : (
          <div className="grid gap-4">
            {documents.items.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <DocumentIcon
                    className={clsx('h-8 w-8', getFileIcon(doc.filename))}
                  />
                  <div>
                    <p className="font-medium text-gray-900">{doc.filename}</p>
                    <div className="flex items-center space-x-4 mt-1">
                      <span className="text-sm text-gray-500">
                        {(doc.file_size / 1024 / 1024).toFixed(2)} MB
                      </span>
                      <span className="text-sm text-gray-500">
                        {new Date(doc.created_at).toLocaleDateString()}
                      </span>
                      {getParseStatus(doc)}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  {doc.parse_status !== 'completed' &&
                    doc.parse_status !== 'parsing' && (
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => parseMutation.mutate(doc.id)}
                        loading={parseMutation.isPending}
                      >
                        解析
                      </Button>
                    )}
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSelectedDoc(doc)}
                    leftIcon={<EyeIcon className="h-4 w-4" />}
                  >
                    预览
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      if (confirm('确定要删除此文档吗？')) {
                        deleteMutation.mutate(doc.id)
                      }
                    }}
                    leftIcon={<TrashIcon className="h-4 w-4 text-red-500" />}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Preview modal */}
      <Modal
        isOpen={!!selectedDoc}
        onClose={() => setSelectedDoc(null)}
        title={selectedDoc?.filename || '文档预览'}
        size="xl"
      >
        {selectedDoc && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-500">文件类型:</span>
                <span className="ml-2 font-medium">{selectedDoc.file_type}</span>
              </div>
              <div>
                <span className="text-gray-500">文件大小:</span>
                <span className="ml-2 font-medium">
                  {(selectedDoc.file_size / 1024 / 1024).toFixed(2)} MB
                </span>
              </div>
              <div>
                <span className="text-gray-500">上传时间:</span>
                <span className="ml-2 font-medium">
                  {new Date(selectedDoc.created_at).toLocaleString()}
                </span>
              </div>
              <div>
                <span className="text-gray-500">解析状态:</span>
                <span className="ml-2">{getParseStatus(selectedDoc)}</span>
              </div>
            </div>

            {selectedDoc.parse_result && (
              <div className="mt-4">
                <h4 className="font-medium text-gray-900 mb-2">解析结果</h4>
                <pre className="bg-gray-50 p-4 rounded-lg text-sm overflow-auto max-h-96">
                  {typeof selectedDoc.parse_result === 'string'
                    ? selectedDoc.parse_result
                    : JSON.stringify(selectedDoc.parse_result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}
