import { clsx } from 'clsx'

type BadgeVariant =
  | 'default'
  | 'primary'
  | 'success'
  | 'warning'
  | 'danger'
  | 'info'

interface BadgeProps {
  children: React.ReactNode
  variant?: BadgeVariant
  size?: 'sm' | 'md'
  className?: string
}

const variantClasses: Record<BadgeVariant, string> = {
  default: 'bg-gray-100 text-gray-800',
  primary: 'bg-primary-100 text-primary-800',
  success: 'bg-green-100 text-green-800',
  warning: 'bg-yellow-100 text-yellow-800',
  danger: 'bg-red-100 text-red-800',
  info: 'bg-blue-100 text-blue-800',
}

const sizeClasses = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-0.5 text-sm',
}

export default function Badge({
  children,
  variant = 'default',
  size = 'sm',
  className,
}: BadgeProps) {
  return (
    <span
      className={clsx(
        'inline-flex items-center font-medium rounded-full',
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
    >
      {children}
    </span>
  )
}

// Risk-specific badges
export function RiskBadge({ level }: { level: number | string }) {
  const numLevel = typeof level === 'string' ? parseInt(level) : level

  const config: Record<number, { label: string; variant: BadgeVariant }> = {
    1: { label: '可接受', variant: 'default' },
    2: { label: '低', variant: 'success' },
    3: { label: '中', variant: 'warning' },
    4: { label: '高', variant: 'danger' },
    5: { label: '严重', variant: 'danger' },
  }

  const { label, variant } = config[numLevel] || { label: '未知', variant: 'default' }

  return <Badge variant={variant}>{label}</Badge>
}

// Status badges
export function StatusBadge({ status }: { status: string }) {
  const config: Record<string, { label: string; variant: BadgeVariant }> = {
    draft: { label: '草稿', variant: 'default' },
    analyzing: { label: '分析中', variant: 'info' },
    completed: { label: '已完成', variant: 'success' },
    pending: { label: '待处理', variant: 'warning' },
    confirmed: { label: '已确认', variant: 'success' },
    not_implemented: { label: '未实施', variant: 'default' },
    in_progress: { label: '实施中', variant: 'info' },
    implemented: { label: '已实施', variant: 'success' },
  }

  const { label, variant } = config[status] || { label: status, variant: 'default' }

  return <Badge variant={variant}>{label}</Badge>
}
