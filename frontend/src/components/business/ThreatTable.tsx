import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  SparklesIcon,
  PencilSquareIcon,
  TrashIcon,
  CheckIcon,
  ExclamationTriangleIcon,
  ChevronDownIcon,
  ChevronUpIcon,
} from '@heroicons/react/24/outline'
import { threatService, Threat, ThreatUpdate } from '@/services/threatService'
import Button from '@/components/common/Button'
import Modal, { ModalFooter } from '@/components/common/Modal'
import Select from '@/components/common/Select'
import Loading from '@/components/common/Loading'
import Pagination from '@/components/common/Pagination'
import { RiskBadge, StatusBadge } from '@/components/common/Badge'
import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableHeaderCell,
  TableCell,
  TableEmpty,
} from '@/components/common/Table'

interface ThreatTableProps {
  projectId: number
}

const strideOptions = [
  { value: '', label: '全部类型' },
  { value: 'S', label: 'Spoofing (欺骗)' },
  { value: 'T', label: 'Tampering (篡改)' },
  { value: 'R', label: 'Repudiation (抵赖)' },
  { value: 'I', label: 'Info Disclosure (信息泄露)' },
  { value: 'D', label: 'Denial of Service (拒绝服务)' },
  { value: 'E', label: 'Elevation of Privilege (权限提升)' },
]

const riskOptions = [
  { value: '', label: '全部风险等级' },
  { value: '5', label: '严重' },
  { value: '4', label: '高' },
  { value: '3', label: '中' },
  { value: '2', label: '低' },
  { value: '1', label: '可接受' },
]

export default function ThreatTable({ projectId }: ThreatTableProps) {
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [strideFilter, setStrideFilter] = useState('')
  const [riskFilter, setRiskFilter] = useState('')
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set())
  const [editingThreat, setEditingThreat] = useState<Threat | null>(null)
  const queryClient = useQueryClient()

  const { data: threats, isLoading } = useQuery({
    queryKey: ['threats', projectId, page, pageSize, strideFilter, riskFilter],
    queryFn: () =>
      threatService.list(projectId, {
        page,
        page_size: pageSize,
        stride_type: strideFilter || undefined,
        risk_level: riskFilter ? parseInt(riskFilter) : undefined,
      }),
  })

  const deleteMutation = useMutation({
    mutationFn: (threatId: number) => threatService.delete(projectId, threatId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threats', projectId] })
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ThreatUpdate }) =>
      threatService.update(projectId, id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threats', projectId] })
      setEditingThreat(null)
    },
  })

  const analyzeMutation = useMutation({
    mutationFn: () => threatService.analyze(projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threats', projectId] })
    },
  })

  const toggleRow = (id: number) => {
    const newExpanded = new Set(expandedRows)
    if (newExpanded.has(id)) {
      newExpanded.delete(id)
    } else {
      newExpanded.add(id)
    }
    setExpandedRows(newExpanded)
  }

  const getStrideColor = (type: string) => {
    const colors: Record<string, string> = {
      S: 'bg-red-100 text-red-800',
      T: 'bg-orange-100 text-orange-800',
      R: 'bg-yellow-100 text-yellow-800',
      I: 'bg-blue-100 text-blue-800',
      D: 'bg-purple-100 text-purple-800',
      E: 'bg-pink-100 text-pink-800',
    }
    return colors[type] || 'bg-gray-100 text-gray-800'
  }

  const renderExpandedContent = (threat: Threat) => (
    <TableRow hover={false}>
      <TableCell colSpan={7} className="bg-gray-50">
        <div className="grid grid-cols-2 gap-6 p-4">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">威胁详情</h4>
            <dl className="space-y-2 text-sm">
              <div>
                <dt className="text-gray-500">损害场景</dt>
                <dd className="text-gray-900">{threat.damage_scenario || '-'}</dd>
              </div>
              <div>
                <dt className="text-gray-500">攻击路径</dt>
                <dd className="text-gray-900">{threat.attack_path || '-'}</dd>
              </div>
              <div>
                <dt className="text-gray-500">WP29映射</dt>
                <dd className="text-gray-900">{threat.wp29_mapping || '-'}</dd>
              </div>
            </dl>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 mb-2">风险评估</h4>
            <dl className="space-y-2 text-sm">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <dt className="text-gray-500">攻击向量</dt>
                  <dd className="text-gray-900">{threat.attack_vector || '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">攻击复杂度</dt>
                  <dd className="text-gray-900">{threat.attack_complexity || '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">权限需求</dt>
                  <dd className="text-gray-900">{threat.privileges_required || '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">用户交互</dt>
                  <dd className="text-gray-900">{threat.user_interaction || '-'}</dd>
                </div>
              </div>
              <div className="grid grid-cols-4 gap-2 pt-2">
                <div>
                  <dt className="text-gray-500">Safety</dt>
                  <dd className="text-gray-900">{threat.impact_safety || '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">Financial</dt>
                  <dd className="text-gray-900">{threat.impact_financial || '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">Operational</dt>
                  <dd className="text-gray-900">{threat.impact_operational || '-'}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">Privacy</dt>
                  <dd className="text-gray-900">{threat.impact_privacy || '-'}</dd>
                </div>
              </div>
            </dl>
          </div>

          {threat.mitigations && threat.mitigations.length > 0 && (
            <div className="col-span-2">
              <h4 className="font-medium text-gray-900 mb-2">安全措施</h4>
              <div className="space-y-2">
                {threat.mitigations.map((m) => (
                  <div
                    key={m.id}
                    className="p-3 bg-white rounded border border-gray-200"
                  >
                    <p className="font-medium text-sm">{m.security_goal}</p>
                    <p className="text-sm text-gray-600 mt-1">
                      {m.security_requirement}
                    </p>
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-xs text-gray-500">
                        WP29: {m.wp29_control_mapping || '-'}
                      </span>
                      <StatusBadge status={m.implementation_status} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </TableCell>
    </TableRow>
  )

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Select
            value={strideFilter}
            onChange={(e) => setStrideFilter(e.target.value)}
            options={strideOptions}
            className="w-48"
          />
          <Select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            options={riskOptions}
            className="w-40"
          />
        </div>
        <Button
          onClick={() => analyzeMutation.mutate()}
          loading={analyzeMutation.isPending}
          leftIcon={<SparklesIcon className="h-4 w-4" />}
        >
          AI 分析
        </Button>
      </div>

      {/* Table */}
      {isLoading ? (
        <Loading text="加载威胁列表..." />
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <Table>
            <TableHead>
              <TableRow hover={false}>
                <TableHeaderCell className="w-8" />
                <TableHeaderCell>威胁ID</TableHeaderCell>
                <TableHeaderCell>关联资产</TableHeaderCell>
                <TableHeaderCell>STRIDE</TableHeaderCell>
                <TableHeaderCell>威胁描述</TableHeaderCell>
                <TableHeaderCell>风险等级</TableHeaderCell>
                <TableHeaderCell align="right">操作</TableHeaderCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {!threats?.items?.length ? (
                <TableEmpty
                  colSpan={7}
                  message="暂无威胁数据，请先完成资产识别后执行 AI 分析"
                />
              ) : (
                threats.items.flatMap((threat) => [
                  <TableRow key={threat.id} onClick={() => toggleRow(threat.id)}>
                    <TableCell>
                      <button className="p-1">
                        {expandedRows.has(threat.id) ? (
                          <ChevronUpIcon className="h-4 w-4 text-gray-400" />
                        ) : (
                          <ChevronDownIcon className="h-4 w-4 text-gray-400" />
                        )}
                      </button>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <ExclamationTriangleIcon className="h-5 w-5 mr-2 text-yellow-500" />
                        <span className="font-mono text-sm">{threat.threat_id}</span>
                      </div>
                    </TableCell>
                    <TableCell>{threat.asset_name || '-'}</TableCell>
                    <TableCell>
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getStrideColor(
                          threat.stride_type
                        )}`}
                      >
                        {threat.stride_type}
                      </span>
                    </TableCell>
                    <TableCell>
                      <p className="truncate max-w-xs">{threat.threat_description}</p>
                    </TableCell>
                    <TableCell>
                      <RiskBadge level={threat.risk_level || 0} />
                    </TableCell>
                    <TableCell align="right">
                      <div
                        className="flex items-center justify-end gap-2"
                        onClick={(e) => e.stopPropagation()}
                      >
                        {!threat.is_confirmed && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() =>
                              updateMutation.mutate({
                                id: threat.id,
                                data: { is_confirmed: true },
                              })
                            }
                            leftIcon={<CheckIcon className="h-4 w-4 text-green-500" />}
                          />
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setEditingThreat(threat)}
                          leftIcon={<PencilSquareIcon className="h-4 w-4" />}
                        />
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => {
                            if (confirm('确定要删除此威胁吗？')) {
                              deleteMutation.mutate(threat.id)
                            }
                          }}
                          leftIcon={<TrashIcon className="h-4 w-4 text-red-500" />}
                        />
                      </div>
                    </TableCell>
                  </TableRow>,
                  expandedRows.has(threat.id) && renderExpandedContent(threat),
                ])
              )}
            </TableBody>
          </Table>

          {threats && threats.total > pageSize && (
            <Pagination
              currentPage={page}
              totalPages={Math.ceil(threats.total / pageSize)}
              totalItems={threats.total}
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

      {/* Edit Modal */}
      <Modal
        isOpen={!!editingThreat}
        onClose={() => setEditingThreat(null)}
        title="编辑威胁"
        size="xl"
      >
        {editingThreat && (
          <>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    威胁ID
                  </label>
                  <p className="mt-1 text-sm text-gray-900">
                    {editingThreat.threat_id}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    关联资产
                  </label>
                  <p className="mt-1 text-sm text-gray-900">
                    {editingThreat.asset_name}
                  </p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  威胁描述
                </label>
                <p className="mt-1 text-sm text-gray-900">
                  {editingThreat.threat_description}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  处置决策
                </label>
                <Select
                  value={editingThreat.treatment_decision || ''}
                  onChange={(e) =>
                    setEditingThreat({
                      ...editingThreat,
                      treatment_decision: e.target.value,
                    })
                  }
                  options={[
                    { value: '', label: '选择处置决策' },
                    { value: 'avoid', label: '规避' },
                    { value: 'reduce', label: '降低' },
                    { value: 'share', label: '转移' },
                    { value: 'accept', label: '接受' },
                  ]}
                />
              </div>
            </div>

            <ModalFooter>
              <Button variant="secondary" onClick={() => setEditingThreat(null)}>
                取消
              </Button>
              <Button
                onClick={() =>
                  updateMutation.mutate({
                    id: editingThreat.id,
                    data: {
                      treatment_decision: editingThreat.treatment_decision,
                    },
                  })
                }
                loading={updateMutation.isPending}
              >
                保存
              </Button>
            </ModalFooter>
          </>
        )}
      </Modal>
    </div>
  )
}
