import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline'
import { clsx } from 'clsx'

interface PaginationProps {
  currentPage: number
  totalPages: number
  totalItems: number
  pageSize: number
  onPageChange: (page: number) => void
  onPageSizeChange?: (size: number) => void
  pageSizeOptions?: number[]
  className?: string
}

export default function Pagination({
  currentPage,
  totalPages,
  totalItems,
  pageSize,
  onPageChange,
  onPageSizeChange,
  pageSizeOptions = [10, 20, 50, 100],
  className,
}: PaginationProps) {
  const startItem = (currentPage - 1) * pageSize + 1
  const endItem = Math.min(currentPage * pageSize, totalItems)

  const getPageNumbers = () => {
    const pages: (number | string)[] = []
    const maxVisible = 5

    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      if (currentPage <= 3) {
        for (let i = 1; i <= 4; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(totalPages)
      } else if (currentPage >= totalPages - 2) {
        pages.push(1)
        pages.push('...')
        for (let i = totalPages - 3; i <= totalPages; i++) {
          pages.push(i)
        }
      } else {
        pages.push(1)
        pages.push('...')
        for (let i = currentPage - 1; i <= currentPage + 1; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(totalPages)
      }
    }

    return pages
  }

  return (
    <div
      className={clsx(
        'flex items-center justify-between py-3 px-4 bg-white border-t border-gray-200',
        className
      )}
    >
      <div className="flex items-center text-sm text-gray-500">
        <span>
          显示 {startItem} - {endItem} 共 {totalItems} 条
        </span>
        {onPageSizeChange && (
          <select
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
            className="ml-4 rounded-md border-gray-300 text-sm focus:border-primary-500 focus:ring-primary-500"
          >
            {pageSizeOptions.map((size) => (
              <option key={size} value={size}>
                每页 {size} 条
              </option>
            ))}
          </select>
        )}
      </div>

      <nav className="flex items-center space-x-1">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className={clsx(
            'p-2 rounded-md text-gray-500',
            currentPage === 1
              ? 'opacity-50 cursor-not-allowed'
              : 'hover:bg-gray-100'
          )}
        >
          <ChevronLeftIcon className="h-4 w-4" />
        </button>

        {getPageNumbers().map((page, index) => (
          <button
            key={index}
            onClick={() => typeof page === 'number' && onPageChange(page)}
            disabled={typeof page !== 'number'}
            className={clsx(
              'px-3 py-1 rounded-md text-sm font-medium',
              page === currentPage
                ? 'bg-primary-600 text-white'
                : typeof page === 'number'
                ? 'text-gray-500 hover:bg-gray-100'
                : 'text-gray-400 cursor-default'
            )}
          >
            {page}
          </button>
        ))}

        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className={clsx(
            'p-2 rounded-md text-gray-500',
            currentPage === totalPages
              ? 'opacity-50 cursor-not-allowed'
              : 'hover:bg-gray-100'
          )}
        >
          <ChevronRightIcon className="h-4 w-4" />
        </button>
      </nav>
    </div>
  )
}
