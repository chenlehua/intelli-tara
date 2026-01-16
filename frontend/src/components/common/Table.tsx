import { ReactNode } from 'react'
import { clsx } from 'clsx'

// Table Container
interface TableProps {
  children: ReactNode
  className?: string
}

export function Table({ children, className }: TableProps) {
  return (
    <div className="overflow-x-auto">
      <table className={clsx('min-w-full divide-y divide-gray-200', className)}>
        {children}
      </table>
    </div>
  )
}

// Table Header
interface TableHeadProps {
  children: ReactNode
  className?: string
}

export function TableHead({ children, className }: TableHeadProps) {
  return <thead className={clsx('bg-gray-50', className)}>{children}</thead>
}

// Table Body
interface TableBodyProps {
  children: ReactNode
  className?: string
}

export function TableBody({ children, className }: TableBodyProps) {
  return (
    <tbody className={clsx('bg-white divide-y divide-gray-200', className)}>
      {children}
    </tbody>
  )
}

// Table Row
interface TableRowProps {
  children: ReactNode
  className?: string
  onClick?: () => void
  hover?: boolean
}

export function TableRow({
  children,
  className,
  onClick,
  hover = true,
}: TableRowProps) {
  return (
    <tr
      className={clsx(
        hover && 'hover:bg-gray-50',
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {children}
    </tr>
  )
}

// Table Header Cell
interface TableHeaderCellProps {
  children?: ReactNode
  className?: string
  align?: 'left' | 'center' | 'right'
}

export function TableHeaderCell({
  children,
  className,
  align = 'left',
}: TableHeaderCellProps) {
  return (
    <th
      scope="col"
      className={clsx(
        'px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider',
        align === 'left' && 'text-left',
        align === 'center' && 'text-center',
        align === 'right' && 'text-right',
        className
      )}
    >
      {children}
    </th>
  )
}

// Table Cell
interface TableCellProps {
  children?: ReactNode
  className?: string
  align?: 'left' | 'center' | 'right'
  colSpan?: number
}

export function TableCell({
  children,
  className,
  align = 'left',
  colSpan,
}: TableCellProps) {
  return (
    <td
      colSpan={colSpan}
      className={clsx(
        'px-4 py-3 text-sm text-gray-900 whitespace-nowrap',
        align === 'left' && 'text-left',
        align === 'center' && 'text-center',
        align === 'right' && 'text-right',
        className
      )}
    >
      {children}
    </td>
  )
}

// Empty State
interface TableEmptyProps {
  message?: string
  colSpan?: number
}

export function TableEmpty({
  message = '暂无数据',
  colSpan = 1,
}: TableEmptyProps) {
  return (
    <tr>
      <td colSpan={colSpan} className="px-4 py-12 text-center text-gray-500">
        {message}
      </td>
    </tr>
  )
}
