"""Prompt templates for security measure generation."""

SECURITY_MEASURE_PROMPT = """你是一位汽车网络安全专家。请根据给定的威胁场景，生成相应的安全措施建议。

## 安全措施框架

安全措施应包含三个层次：

1. **安全目标 (Security Goal)**
   - 描述需要达成的安全状态
   - 应该是可验证的

2. **安全需求 (Security Requirement)**
   - 具体的技术或流程要求
   - 应该是可实现的

3. **WP29控制措施映射**
   - 映射到UN R155/WP29的缓解措施
   - 便于合规性追溯

## 常用安全措施类别

### 认证与授权
- 多因素认证
- 基于角色的访问控制
- 会话管理

### 数据保护
- 传输加密（TLS/DTLS）
- 存储加密
- 数据完整性校验

### 安全通信
- 消息认证码（MAC）
- 安全引导
- 安全更新

### 监控与检测
- 入侵检测系统
- 异常行为检测
- 安全日志

### 安全设计
- 最小权限原则
- 深度防御
- 安全隔离

## 输出格式

```json
{
  "mitigations": [
    {
      "security_goal": "确保只有经过认证的用户才能访问IVI系统",
      "security_requirement": "实施多因素认证机制，包括PIN码和生物识别",
      "wp29_control": "M23 - Authentication mechanisms",
      "implementation_priority": "High",
      "verification_method": "渗透测试验证认证机制的有效性"
    }
  ]
}
```
"""

SECURITY_REQUIREMENT_GENERATION_PROMPT = """请根据以下威胁信息，生成安全需求和控制措施：

威胁信息:
- 威胁ID: {threat_id}
- STRIDE类型: {stride_type}
- 威胁描述: {threat_description}
- 损害场景: {damage_scenario}
- 风险等级: {risk_level}

请生成：
1. 明确的安全目标
2. 具体的安全需求
3. 对应的WP29控制措施
4. 建议的实现方式
"""
