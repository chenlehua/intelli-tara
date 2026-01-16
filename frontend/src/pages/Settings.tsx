import { useAuthStore } from '@/stores/authStore'

export default function Settings() {
  const { user } = useAuthStore()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">系统设置</h1>
        <p className="mt-1 text-sm text-gray-500">管理您的账户和系统配置</p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">个人信息</h2>
        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">用户名</dt>
            <dd className="mt-1 text-sm text-gray-900">{user?.username}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">邮箱</dt>
            <dd className="mt-1 text-sm text-gray-900">{user?.email}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">显示名称</dt>
            <dd className="mt-1 text-sm text-gray-900">{user?.display_name || '-'}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">角色</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {user?.roles?.join(', ') || '-'}
            </dd>
          </div>
        </dl>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">系统信息</h2>
        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">版本</dt>
            <dd className="mt-1 text-sm text-gray-900">1.0.0</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">基于标准</dt>
            <dd className="mt-1 text-sm text-gray-900">ISO/SAE 21434:2021</dd>
          </div>
        </dl>
      </div>
    </div>
  )
}
