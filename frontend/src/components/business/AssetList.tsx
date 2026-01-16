import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  PlusIcon,
  SparklesIcon,
  PencilSquareIcon,
  TrashIcon,
  CheckIcon,
  CubeIcon,
} from '@heroicons/react/24/outline'
import { assetService, Asset, AssetCreate, AssetUpdate } from '@/services/assetService'
import Button from '@/components/common/Button'
import Modal, { ModalFooter } from '@/components/common/Modal'
import Input from '@/components/common/Input'
import Select from '@/components/common/Select'
import Loading from '@/components/common/Loading'
import Pagination from '@/components/common/Pagination'
import { StatusBadge } from '@/components/common/Badge'
import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableHeaderCell,
  TableCell,
  TableEmpty,
} from '@/components/common/Table'

interface AssetListProps {
  projectId: number
}

const categoryOptions = [
  { value: 'hardware', label: '硬件' },
  { value: 'software', label: '软件' },
  { value: 'data', label: '数据' },
  { value: 'interface', label: '接口' },
  { value: 'function', label: '功能' },
]

const defaultAsset: AssetCreate = {
  asset_id: '',
  name: '',
  category: 'software',
  description: '',
  authenticity: true,
  integrity: true,
  confidentiality: true,
  availability: true,
}

export default function AssetList({ projectId }: AssetListProps) {
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [categoryFilter, setCategoryFilter] = useState('')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingAsset, setEditingAsset] = useState<Asset | null>(null)
  const [formData, setFormData] = useState<AssetCreate>(defaultAsset)
  const queryClient = useQueryClient()

  const { data: assets, isLoading } = useQuery({
    queryKey: ['assets', projectId, page, pageSize, categoryFilter],
    queryFn: () =>
      assetService.list(projectId, {
        page,
        page_size: pageSize,
        category: categoryFilter || undefined,
      }),
  })

  const createMutation = useMutation({
    mutationFn: (data: AssetCreate) => assetService.create(projectId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets', projectId] })
      setShowCreateModal(false)
      setFormData(defaultAsset)
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: AssetUpdate }) =>
      assetService.update(projectId, id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets', projectId] })
      setEditingAsset(null)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (assetId: number) => assetService.delete(projectId, assetId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets', projectId] })
    },
  })

  const confirmMutation = useMutation({
    mutationFn: (assetId: number) => assetService.confirm(projectId, assetId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets', projectId] })
    },
  })

  const identifyMutation = useMutation({
    mutationFn: () => assetService.identify(projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets', projectId] })
    },
  })

  const handleCreate = () => {
    if (formData.name && formData.asset_id) {
      createMutation.mutate(formData)
    }
  }

  const handleUpdate = () => {
    if (editingAsset) {
      updateMutation.mutate({ id: editingAsset.id, data: formData as AssetUpdate })
    }
  }

  const openEditModal = (asset: Asset) => {
    setEditingAsset(asset)
    setFormData({
      asset_id: asset.asset_id,
      name: asset.name,
      category: asset.category,
      subcategory: asset.subcategory,
      description: asset.description,
      remarks: asset.remarks,
      authenticity: asset.authenticity,
      integrity: asset.integrity,
      non_repudiation: asset.non_repudiation,
      confidentiality: asset.confidentiality,
      availability: asset.availability,
      authorization: asset.authorization,
    })
  }

  const renderSecurityAttributes = (asset: Asset) => {
    const attrs = [
      { key: 'authenticity', label: '真', value: asset.authenticity },
      { key: 'integrity', label: '完', value: asset.integrity },
      { key: 'confidentiality', label: '机', value: asset.confidentiality },
      { key: 'availability', label: '可', value: asset.availability },
      { key: 'non_repudiation', label: '不', value: asset.non_repudiation },
      { key: 'authorization', label: '权', value: asset.authorization },
    ]

    return (
      <div className="flex gap-1">
        {attrs.map((attr) => (
          <span
            key={attr.key}
            className={`w-6 h-6 flex items-center justify-center rounded text-xs font-medium ${
              attr.value
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-400'
            }`}
            title={attr.label}
          >
            {attr.value ? '✓' : '-'}
          </span>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            options={[{ value: '', label: '全部分类' }, ...categoryOptions]}
            className="w-40"
          />
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            onClick={() => setShowCreateModal(true)}
            leftIcon={<PlusIcon className="h-4 w-4" />}
          >
            手动添加
          </Button>
          <Button
            onClick={() => identifyMutation.mutate()}
            loading={identifyMutation.isPending}
            leftIcon={<SparklesIcon className="h-4 w-4" />}
          >
            AI 识别
          </Button>
        </div>
      </div>

      {/* Table */}
      {isLoading ? (
        <Loading text="加载资产列表..." />
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <Table>
            <TableHead>
              <TableRow hover={false}>
                <TableHeaderCell>资产ID</TableHeaderCell>
                <TableHeaderCell>资产名称</TableHeaderCell>
                <TableHeaderCell>分类</TableHeaderCell>
                <TableHeaderCell>安全属性</TableHeaderCell>
                <TableHeaderCell>状态</TableHeaderCell>
                <TableHeaderCell align="right">操作</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {!assets?.items?.length ? (
                <TableEmpty colSpan={6} message="暂无资产数据，请上传文档后执行 AI 识别" />
              ) : (
                assets.items.map((asset) => (
                  <TableRow key={asset.id}>
                    <TableCell>
                      <div className="flex items-center">
                        <CubeIcon className="h-5 w-5 mr-2 text-gray-400" />
                        <span className="font-mono text-sm">{asset.asset_id}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div>
                        <p className="font-medium">{asset.name}</p>
                        {asset.description && (
                          <p className="text-xs text-gray-500 truncate max-w-xs">
                            {asset.description}
                          </p>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="capitalize">{asset.category}</span>
                      {asset.subcategory && (
                        <span className="text-gray-400"> / {asset.subcategory}</span>
                      )}
                    </TableCell>
                    <TableCell>{renderSecurityAttributes(asset)}</TableCell>
                    <TableCell>
                      {asset.is_confirmed ? (
                        <StatusBadge status="confirmed" />
                      ) : asset.is_ai_generated ? (
                        <StatusBadge status="pending" />
                      ) : (
                        <StatusBadge status="draft" />
                      )}
                    </TableCell>
                    <TableCell align="right">
                      <div className="flex items-center justify-end gap-2">
                        {!asset.is_confirmed && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => confirmMutation.mutate(asset.id)}
                            leftIcon={<CheckIcon className="h-4 w-4 text-green-500" />}
                          />
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => openEditModal(asset)}
                          leftIcon={<PencilSquareIcon className="h-4 w-4" />}
                        />
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => {
                            if (confirm('确定要删除此资产吗？')) {
                              deleteMutation.mutate(asset.id)
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

          {assets && assets.total > pageSize && (
            <Pagination
              currentPage={page}
              totalPages={Math.ceil(assets.total / pageSize)}
              totalItems={assets.total}
              pageSize={pageSize}
              onPageChange={setPage}
              onPageSizeChange={(size) => {
                setPageSize(size)
                setPage(1)
              }}
            />
          )}
        </div>
      )}

      {/* Create/Edit Modal */}
      <Modal
        isOpen={showCreateModal || !!editingAsset}
        onClose={() => {
          setShowCreateModal(false)
          setEditingAsset(null)
          setFormData(defaultAsset)
        }}
        title={editingAsset ? '编辑资产' : '添加资产'}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="资产ID *"
              value={formData.asset_id}
              onChange={(e) =>
                setFormData({ ...formData, asset_id: e.target.value })
              }
              placeholder="例如: AST-001"
            />
            <Input
              label="资产名称 *"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              placeholder="请输入资产名称"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Select
              label="分类"
              value={formData.category}
              onChange={(e) =>
                setFormData({ ...formData, category: e.target.value })
              }
              options={categoryOptions}
            />
            <Input
              label="子分类"
              value={formData.subcategory || ''}
              onChange={(e) =>
                setFormData({ ...formData, subcategory: e.target.value })
              }
              placeholder="请输入子分类"
            />
          </div>

          <Input
            label="描述"
            value={formData.description || ''}
            onChange={(e) =>
              setFormData({ ...formData, description: e.target.value })
            }
            placeholder="请输入资产描述"
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              安全属性
            </label>
            <div className="flex flex-wrap gap-4">
              {[
                { key: 'authenticity', label: '真实性' },
                { key: 'integrity', label: '完整性' },
                { key: 'confidentiality', label: '机密性' },
                { key: 'availability', label: '可用性' },
                { key: 'non_repudiation', label: '不可抵赖性' },
                { key: 'authorization', label: '权限控制' },
              ].map((attr) => (
                <label key={attr.key} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData[attr.key as keyof AssetCreate] as boolean}
                    onChange={(e) =>
                      setFormData({ ...formData, [attr.key]: e.target.checked })
                    }
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{attr.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        <ModalFooter>
          <Button
            variant="secondary"
            onClick={() => {
              setShowCreateModal(false)
              setEditingAsset(null)
              setFormData(defaultAsset)
            }}
          >
            取消
          </Button>
          <Button
            onClick={editingAsset ? handleUpdate : handleCreate}
            loading={createMutation.isPending || updateMutation.isPending}
          >
            {editingAsset ? '保存' : '创建'}
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  )
}
