import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import {
  UserIcon,
  KeyIcon,
  BellIcon,
  InformationCircleIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline'
import { useAuthStore } from '@/stores/authStore'
import { authService } from '@/services/authService'
import Button from '@/components/common/Button'
import Input from '@/components/common/Input'
import Card, { CardHeader } from '@/components/common/Card'
import Tabs from '@/components/common/Tabs'
import Modal, { ModalFooter } from '@/components/common/Modal'
import { useToast } from '@/components/common/Toast'

const tabs = [
  { key: 'profile', label: '个人信息', icon: <UserIcon className="h-4 w-4" /> },
  { key: 'security', label: '安全设置', icon: <KeyIcon className="h-4 w-4" /> },
  { key: 'notifications', label: '通知设置', icon: <BellIcon className="h-4 w-4" /> },
  { key: 'about', label: '关于系统', icon: <InformationCircleIcon className="h-4 w-4" /> },
]

export default function Settings() {
  const { user } = useAuthStore()
  const toast = useToast()
  const [activeTab, setActiveTab] = useState('profile')
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  })

  const changePasswordMutation = useMutation({
    mutationFn: (data: { current_password: string; new_password: string }) =>
      authService.changePassword(data),
    onSuccess: () => {
      toast.success('密码修改成功')
      setShowPasswordModal(false)
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' })
    },
    onError: () => {
      toast.error('密码修改失败，请检查当前密码是否正确')
    },
  })

  const handleChangePassword = () => {
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error('两次输入的新密码不一致')
      return
    }
    if (passwordData.newPassword.length < 6) {
      toast.error('密码长度不能少于6位')
      return
    }
    changePasswordMutation.mutate({
      current_password: passwordData.currentPassword,
      new_password: passwordData.newPassword,
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">系统设置</h1>
        <p className="mt-1 text-sm text-gray-500">管理您的账户和系统配置</p>
      </div>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

      <div className="mt-6">
        {activeTab === 'profile' && (
          <Card padding="lg">
            <CardHeader title="个人信息" description="查看和编辑您的个人资料" />
            <dl className="grid grid-cols-1 gap-6 sm:grid-cols-2">
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
                <dd className="mt-1 text-sm text-gray-900">
                  {user?.display_name || '-'}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">角色</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {user?.roles?.join(', ') || '-'}
                </dd>
              </div>
            </dl>
          </Card>
        )}

        {activeTab === 'security' && (
          <Card padding="lg">
            <CardHeader title="安全设置" description="管理您的密码和安全选项" />
            <div className="space-y-6">
              <div className="flex items-center justify-between py-4 border-b border-gray-200">
                <div>
                  <h3 className="text-sm font-medium text-gray-900">修改密码</h3>
                  <p className="text-sm text-gray-500">
                    定期更换密码可以提高账户安全性
                  </p>
                </div>
                <Button
                  variant="secondary"
                  onClick={() => setShowPasswordModal(true)}
                >
                  修改密码
                </Button>
              </div>

              <div className="flex items-center justify-between py-4 border-b border-gray-200">
                <div>
                  <h3 className="text-sm font-medium text-gray-900">
                    两步验证
                  </h3>
                  <p className="text-sm text-gray-500">
                    启用两步验证以增强账户安全
                  </p>
                </div>
                <Button variant="secondary" disabled>
                  即将推出
                </Button>
              </div>

              <div className="flex items-center justify-between py-4">
                <div>
                  <h3 className="text-sm font-medium text-gray-900">
                    登录历史
                  </h3>
                  <p className="text-sm text-gray-500">
                    查看最近的登录记录
                  </p>
                </div>
                <Button variant="secondary" disabled>
                  查看历史
                </Button>
              </div>
            </div>
          </Card>
        )}

        {activeTab === 'notifications' && (
          <Card padding="lg">
            <CardHeader title="通知设置" description="管理系统通知偏好" />
            <div className="space-y-4">
              {[
                { id: 'email', label: '邮件通知', description: '接收重要更新的邮件通知' },
                { id: 'analysis', label: '分析完成', description: '当 AI 分析任务完成时通知' },
                { id: 'report', label: '报告生成', description: '当报告生成完成时通知' },
                { id: 'risk', label: '高风险警告', description: '发现高风险威胁时立即通知' },
              ].map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between py-4 border-b border-gray-200 last:border-0"
                >
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">
                      {item.label}
                    </h3>
                    <p className="text-sm text-gray-500">{item.description}</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </Card>
        )}

        {activeTab === 'about' && (
          <div className="space-y-6">
            <Card padding="lg">
              <CardHeader title="系统信息" />
              <dl className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <dt className="text-sm font-medium text-gray-500">系统名称</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    Intelli-TARA 智能威胁分析与风险评估平台
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">版本</dt>
                  <dd className="mt-1 text-sm text-gray-900">1.0.0</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">遵循标准</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    ISO/SAE 21434:2021, UN R155
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">威胁模型</dt>
                  <dd className="mt-1 text-sm text-gray-900">STRIDE</dd>
                </div>
              </dl>
            </Card>

            <Card padding="lg">
              <CardHeader title="技术支持" />
              <div className="flex items-start space-x-4">
                <ShieldCheckIcon className="h-12 w-12 text-primary-600" />
                <div>
                  <p className="text-sm text-gray-600">
                    Intelli-TARA 是一款基于人工智能的汽车网络安全威胁分析与风险评估平台。
                    系统集成了先进的自然语言处理和计算机视觉技术，能够自动识别系统资产、
                    分析潜在威胁并生成符合行业标准的分析报告。
                  </p>
                  <p className="mt-4 text-sm text-gray-500">
                    如需技术支持，请联系系统管理员。
                  </p>
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>

      {/* Password Modal */}
      <Modal
        isOpen={showPasswordModal}
        onClose={() => setShowPasswordModal(false)}
        title="修改密码"
      >
        <div className="space-y-4">
          <Input
            label="当前密码"
            type="password"
            value={passwordData.currentPassword}
            onChange={(e) =>
              setPasswordData({ ...passwordData, currentPassword: e.target.value })
            }
            placeholder="请输入当前密码"
          />
          <Input
            label="新密码"
            type="password"
            value={passwordData.newPassword}
            onChange={(e) =>
              setPasswordData({ ...passwordData, newPassword: e.target.value })
            }
            placeholder="请输入新密码（至少6位）"
          />
          <Input
            label="确认新密码"
            type="password"
            value={passwordData.confirmPassword}
            onChange={(e) =>
              setPasswordData({ ...passwordData, confirmPassword: e.target.value })
            }
            placeholder="请再次输入新密码"
          />
        </div>

        <ModalFooter>
          <Button
            variant="secondary"
            onClick={() => setShowPasswordModal(false)}
          >
            取消
          </Button>
          <Button
            onClick={handleChangePassword}
            loading={changePasswordMutation.isPending}
          >
            确认修改
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  )
}
