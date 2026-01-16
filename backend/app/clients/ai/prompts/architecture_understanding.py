"""Prompt templates for architecture understanding."""

ARCHITECTURE_UNDERSTANDING_PROMPT = """你是一位汽车电子架构专家。请分析这张汽车电子/电气架构图，提取以下信息：

## 需要识别的信息

1. **系统组件**
   - ECU（电子控制单元）
   - 网关
   - 域控制器
   - 传感器
   - 执行器

2. **通信网络**
   - CAN总线
   - LIN总线
   - FlexRay
   - 车载以太网
   - 无线网络（WiFi/蓝牙/蜂窝）

3. **数据流向**
   - 诊断数据流
   - 控制指令流
   - 娱乐数据流
   - 安全相关数据流

4. **接口和边界**
   - 外部接口（OBD-II, USB等）
   - 网络边界
   - 域边界

## 输出格式

请以JSON格式输出：

```json
{
  "components": [
    {
      "id": "COMP-001",
      "name": "车载信息娱乐系统",
      "type": "ECU",
      "domain": "信息娱乐域",
      "description": "负责导航、多媒体和互联功能"
    }
  ],
  "networks": [
    {
      "id": "NET-001",
      "name": "CAN高速总线",
      "type": "CAN",
      "speed": "500kbps",
      "connected_components": ["COMP-001", "COMP-002"]
    }
  ],
  "data_flows": [
    {
      "id": "FLOW-001",
      "source": "COMP-001",
      "target": "COMP-002",
      "data_type": "诊断数据",
      "protocol": "UDS over CAN"
    }
  ],
  "external_interfaces": [
    {
      "id": "IF-001",
      "name": "OBD-II端口",
      "type": "物理接口",
      "connected_to": "NET-001",
      "access_level": "物理接触"
    }
  ],
  "security_boundaries": [
    {
      "id": "BOUND-001",
      "name": "网关边界",
      "description": "隔离信息娱乐域和动力域",
      "protected_components": ["COMP-003", "COMP-004"]
    }
  ]
}
```

请尽可能详细地分析架构图中的所有元素及其关系。
"""

COMMUNICATION_MATRIX_ANALYSIS_PROMPT = """请分析以下通信矩阵数据，提取资产和通信关系信息。

通信矩阵通常包含以下信息：
- 发送节点
- 接收节点
- 消息ID
- 消息名称
- 周期
- 数据长度
- 信号列表

请识别出：
1. 所有通信节点（作为资产）
2. 节点之间的通信关系
3. 关键的安全相关消息

输出格式：
```json
{
  "nodes": [...],
  "communications": [
    {
      "sender": "Node A",
      "receiver": "Node B",
      "message_id": "0x123",
      "message_name": "VehicleSpeed",
      "cycle_time": 10,
      "is_safety_relevant": true
    }
  ]
}
```
"""
