import { ReactNode } from 'react'
import { clsx } from 'clsx'

interface CardProps {
  children: ReactNode
  className?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hover?: boolean
  onClick?: () => void
}

const paddingClasses = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
}

export default function Card({
  children,
  className,
  padding = 'md',
  hover = false,
  onClick,
}: CardProps) {
  return (
    <div
      className={clsx(
        'bg-white rounded-lg shadow',
        paddingClasses[padding],
        hover && 'transition-shadow hover:shadow-md',
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {children}
    </div>
  )
}

interface CardHeaderProps {
  title: string
  description?: string
  actions?: ReactNode
  className?: string
}

export function CardHeader({
  title,
  description,
  actions,
  className,
}: CardHeaderProps) {
  return (
    <div className={clsx('flex items-center justify-between mb-4', className)}>
      <div>
        <h3 className="text-lg font-medium text-gray-900">{title}</h3>
        {description && (
          <p className="mt-1 text-sm text-gray-500">{description}</p>
        )}
      </div>
      {actions && <div className="flex items-center space-x-2">{actions}</div>}
    </div>
  )
}

interface CardFooterProps {
  children: ReactNode
  className?: string
}

export function CardFooter({ children, className }: CardFooterProps) {
  return (
    <div
      className={clsx(
        'flex items-center justify-end pt-4 mt-4 border-t border-gray-200',
        className
      )}
    >
      {children}
    </div>
  )
}
