import { clsx } from 'clsx'

interface Tab {
  key: string
  label: string
  icon?: React.ReactNode
  disabled?: boolean
}

interface TabsProps {
  tabs: Tab[]
  activeTab: string
  onChange: (key: string) => void
  variant?: 'underline' | 'pills'
  className?: string
}

export default function Tabs({
  tabs,
  activeTab,
  onChange,
  variant = 'underline',
  className,
}: TabsProps) {
  if (variant === 'pills') {
    return (
      <div className={clsx('flex space-x-2', className)}>
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => !tab.disabled && onChange(tab.key)}
            disabled={tab.disabled}
            className={clsx(
              'px-4 py-2 text-sm font-medium rounded-md transition-colors',
              activeTab === tab.key
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100',
              tab.disabled && 'opacity-50 cursor-not-allowed'
            )}
          >
            {tab.icon && <span className="mr-2">{tab.icon}</span>}
            {tab.label}
          </button>
        ))}
      </div>
    )
  }

  return (
    <div className={clsx('border-b border-gray-200', className)}>
      <nav className="-mb-px flex space-x-8">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => !tab.disabled && onChange(tab.key)}
            disabled={tab.disabled}
            className={clsx(
              'flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === tab.key
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              tab.disabled && 'opacity-50 cursor-not-allowed'
            )}
          >
            {tab.icon && <span className="mr-2">{tab.icon}</span>}
            {tab.label}
          </button>
        ))}
      </nav>
    </div>
  )
}
