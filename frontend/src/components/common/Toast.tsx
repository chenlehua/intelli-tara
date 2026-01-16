import { useState, useEffect, createContext, useContext, ReactNode } from 'react'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  XCircleIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { clsx } from 'clsx'

type ToastType = 'success' | 'error' | 'warning' | 'info'

interface Toast {
  id: string
  type: ToastType
  message: string
  duration?: number
}

interface ToastContextValue {
  showToast: (type: ToastType, message: string, duration?: number) => void
  success: (message: string) => void
  error: (message: string) => void
  warning: (message: string) => void
  info: (message: string) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider')
  }
  return context
}

interface ToastProviderProps {
  children: ReactNode
}

export function ToastProvider({ children }: ToastProviderProps) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const showToast = (type: ToastType, message: string, duration = 3000) => {
    const id = Math.random().toString(36).substring(7)
    setToasts((prev) => [...prev, { id, type, message, duration }])
  }

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id))
  }

  const value: ToastContextValue = {
    showToast,
    success: (message) => showToast('success', message),
    error: (message) => showToast('error', message),
    warning: (message) => showToast('warning', message),
    info: (message) => showToast('info', message),
  }

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  )
}

interface ToastContainerProps {
  toasts: Toast[]
  onRemove: (id: string) => void
}

function ToastContainer({ toasts, onRemove }: ToastContainerProps) {
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={onRemove} />
      ))}
    </div>
  )
}

interface ToastItemProps {
  toast: Toast
  onRemove: (id: string) => void
}

function ToastItem({ toast, onRemove }: ToastItemProps) {
  useEffect(() => {
    if (toast.duration) {
      const timer = setTimeout(() => {
        onRemove(toast.id)
      }, toast.duration)
      return () => clearTimeout(timer)
    }
  }, [toast.id, toast.duration, onRemove])

  const icons = {
    success: CheckCircleIcon,
    error: XCircleIcon,
    warning: ExclamationCircleIcon,
    info: InformationCircleIcon,
  }

  const colors = {
    success: 'bg-green-50 text-green-800 border-green-200',
    error: 'bg-red-50 text-red-800 border-red-200',
    warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
    info: 'bg-blue-50 text-blue-800 border-blue-200',
  }

  const iconColors = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500',
  }

  const Icon = icons[toast.type]

  return (
    <div
      className={clsx(
        'flex items-center p-4 rounded-lg border shadow-lg min-w-[300px] max-w-md',
        colors[toast.type]
      )}
    >
      <Icon className={clsx('h-5 w-5 mr-3', iconColors[toast.type])} />
      <span className="flex-1 text-sm">{toast.message}</span>
      <button
        onClick={() => onRemove(toast.id)}
        className="ml-3 text-gray-400 hover:text-gray-500"
      >
        <XMarkIcon className="h-4 w-4" />
      </button>
    </div>
  )
}
