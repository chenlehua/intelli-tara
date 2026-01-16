import { useQuery } from '@tanstack/react-query'
import { threatService } from '@/services/threatService'
import { clsx } from 'clsx'

interface RiskMatrixProps {
  projectId?: number
  data?: {
    matrix?: number[][]
    threat_counts?: Record<number, number>
    total_threats?: number
    high_risk_count?: number
  }
}

// 5x5 Risk Matrix based on ISO 21434
// Rows: Attack Feasibility (1=Very Low to 5=Very High)
// Cols: Impact Level (1=Negligible to 5=Severe)
const RISK_MATRIX = [
  // Impact: Negligible, Minor, Moderate, Major, Severe
  [1, 1, 2, 2, 3], // Feasibility: Very Low
  [1, 2, 2, 3, 3], // Feasibility: Low
  [2, 2, 3, 3, 4], // Feasibility: Medium
  [2, 3, 3, 4, 4], // Feasibility: High
  [3, 3, 4, 4, 5], // Feasibility: Very High
]

const FEASIBILITY_LABELS = ['极低', '低', '中', '高', '极高']
const IMPACT_LABELS = ['可忽略', '轻微', '中等', '重大', '严重']
const RISK_LABELS = ['可接受', '低', '中', '高', '严重']

const RISK_COLORS: Record<number, string> = {
  1: 'bg-gray-200 text-gray-700',
  2: 'bg-green-200 text-green-800',
  3: 'bg-yellow-200 text-yellow-800',
  4: 'bg-orange-200 text-orange-800',
  5: 'bg-red-300 text-red-900',
}

export default function RiskMatrix({ projectId, data }: RiskMatrixProps) {
  const { data: riskData } = useQuery({
    queryKey: ['risk-matrix', projectId],
    queryFn: () => (projectId ? threatService.getRiskMatrix(projectId) : null),
    enabled: !!projectId && !data,
  })

  const matrixData = data || riskData

  // Calculate threat distribution
  const getCount = (_feasibility: number, _impact: number): number => {
    if (!matrixData?.matrix) return 0
    // This would need to be properly calculated from backend
    return 0
  }

  return (
    <div className="space-y-6">
      {/* Risk Matrix */}
      <div className="overflow-x-auto">
        <div className="min-w-[600px]">
          <div className="flex">
            {/* Y-axis label */}
            <div className="w-24 flex items-center justify-center">
              <span
                className="transform -rotate-90 text-sm font-medium text-gray-700 whitespace-nowrap"
                style={{ width: '120px' }}
              >
                攻击可行性 →
              </span>
            </div>

            <div className="flex-1">
              {/* Matrix grid */}
              <div className="space-y-1">
                {FEASIBILITY_LABELS.slice()
                  .reverse()
                  .map((feasLabel, rowIdx) => {
                    const feasibility = 5 - rowIdx
                    return (
                      <div key={feasLabel} className="flex items-center">
                        <div className="w-12 text-right pr-2 text-sm text-gray-600">
                          {feasLabel}
                        </div>
                        <div className="flex-1 flex gap-1">
                          {IMPACT_LABELS.map((impLabel, colIdx) => {
                            const impact = colIdx + 1
                            const riskLevel = RISK_MATRIX[feasibility - 1][impact - 1]
                            const count = getCount(feasibility, impact)

                            return (
                              <div
                                key={impLabel}
                                className={clsx(
                                  'flex-1 h-16 rounded flex flex-col items-center justify-center text-sm font-medium transition-transform hover:scale-105',
                                  RISK_COLORS[riskLevel]
                                )}
                                title={`可行性: ${feasLabel}, 影响: ${impLabel}, 风险: ${RISK_LABELS[riskLevel - 1]}`}
                              >
                                <span>{RISK_LABELS[riskLevel - 1]}</span>
                                {count > 0 && (
                                  <span className="text-xs mt-1">({count})</span>
                                )}
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    )
                  })}

                {/* X-axis labels */}
                <div className="flex items-center mt-2">
                  <div className="w-12" />
                  <div className="flex-1 flex gap-1">
                    {IMPACT_LABELS.map((label) => (
                      <div
                        key={label}
                        className="flex-1 text-center text-sm text-gray-600"
                      >
                        {label}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* X-axis title */}
              <div className="text-center mt-2 text-sm font-medium text-gray-700">
                影响等级 →
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Legend and Statistics */}
      <div className="grid grid-cols-2 gap-6">
        {/* Legend */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">风险等级说明</h4>
          <div className="space-y-2">
            {[5, 4, 3, 2, 1].map((level) => (
              <div key={level} className="flex items-center">
                <div
                  className={clsx(
                    'w-16 h-6 rounded flex items-center justify-center text-xs font-medium',
                    RISK_COLORS[level]
                  )}
                >
                  {RISK_LABELS[level - 1]}
                </div>
                <span className="ml-3 text-sm text-gray-600">
                  {level === 5 && '需要立即处理的严重风险'}
                  {level === 4 && '高优先级处理'}
                  {level === 3 && '需要制定缓解措施'}
                  {level === 2 && '可接受但需监控'}
                  {level === 1 && '无需额外处理'}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Statistics */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">风险分布统计</h4>
          {matrixData?.threat_counts ? (
            <div className="space-y-2">
              {[5, 4, 3, 2, 1].map((level) => {
                const count = matrixData.threat_counts?.[level] || 0
                const total = matrixData.total_threats || 1
                const percentage = Math.round((count / total) * 100)

                return (
                  <div key={level} className="flex items-center">
                    <span
                      className={clsx(
                        'w-16 h-6 rounded flex items-center justify-center text-xs font-medium',
                        RISK_COLORS[level]
                      )}
                    >
                      {RISK_LABELS[level - 1]}
                    </span>
                    <div className="flex-1 mx-3">
                      <div className="h-4 bg-gray-100 rounded overflow-hidden">
                        <div
                          className={clsx(
                            'h-full transition-all',
                            level === 5 && 'bg-red-400',
                            level === 4 && 'bg-orange-400',
                            level === 3 && 'bg-yellow-400',
                            level === 2 && 'bg-green-400',
                            level === 1 && 'bg-gray-400'
                          )}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                    <span className="text-sm text-gray-600 w-16 text-right">
                      {count} ({percentage}%)
                    </span>
                  </div>
                )
              })}
            </div>
          ) : (
            <p className="text-sm text-gray-500">暂无威胁数据</p>
          )}
        </div>
      </div>
    </div>
  )
}
