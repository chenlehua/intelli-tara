"""Prompt templates for asset identification."""

ASSET_IDENTIFICATION_PROMPT = """你是一位汽车网络安全专家，专门负责TARA（威胁分析与风险评估）中的资产识别工作。
请根据提供的文档内容，识别其中涉及的所有资产信息。

## 资产分类体系

请按照以下分类体系对资产进行分类：

1. **硬件资产 (Hardware)**
   - 处理器 (Processor): SOC, MCU, CPU
   - 存储器 (Memory): DDR, Flash, eMMC, SD卡
   - 通信模块 (Communication): 蓝牙模块, WiFi模块, 4G/5G模块, V2X模块
   - 传感器 (Sensor): 摄像头, 雷达, 激光雷达, GPS

2. **软件资产 (Software)**
   - 系统软件 (System): 操作系统, Bootloader, TEE, Hypervisor
   - 中间件 (Middleware): AUTOSAR, ROS, 通信中间件
   - 应用软件 (Application): 导航, 多媒体, 车控App, 第三方应用

3. **数据资产 (Data)**
   - 配置数据 (Config): 系统配置, 用户设置, 网络配置
   - 用户数据 (User): 个人信息, 使用记录, 收藏夹, 通讯录
   - 密钥数据 (Key): 加密密钥, 数字证书, 认证凭证
   - 日志数据 (Log): 系统日志, 诊断数据, 行车记录

4. **接口资产 (Interface)**
   - 有线接口 (Wired): CAN总线, 以太网, USB, UART, JTAG, OBD-II
   - 无线接口 (Wireless): 蓝牙, WiFi, NFC, 蜂窝网络

5. **外部实体 (External)**
   - 外部设备 (Device): OBD诊断设备, 手机, 充电桩
   - 外部服务 (Service): TSP云服务, 第三方服务, OTA服务器

## 安全属性

对于每个资产，请评估以下安全属性是否适用（用true/false表示）：

- **真实性 (Authenticity)**: 是否需要确保实体身份真实可信
- **完整性 (Integrity)**: 是否需要确保数据未被未授权修改
- **不可抵赖性 (Non-repudiation)**: 是否需要确保行为可追溯、不可否认
- **机密性 (Confidentiality)**: 是否需要确保数据不被未授权访问
- **可用性 (Availability)**: 是否需要确保服务持续可用
- **授权性 (Authorization)**: 是否需要确保访问经过适当授权

## 输出格式

请以JSON格式输出，结构如下：

```json
{
  "assets": [
    {
      "asset_id": "HW-001",
      "name": "车载信息娱乐系统主控SOC",
      "category": "硬件资产",
      "subcategory": "处理器",
      "description": "IVI系统的核心处理器，运行Android系统",
      "remarks": "高通8155芯片",
      "authenticity": true,
      "integrity": true,
      "non_repudiation": false,
      "confidentiality": true,
      "availability": true,
      "authorization": true
    }
  ]
}
```

## 资产ID命名规则

- 硬件资产: HW-XXX
- 软件资产: SW-XXX
- 数据资产: DA-XXX
- 接口资产: IF-XXX
- 外部实体: EX-XXX

请仔细分析文档内容，尽可能全面地识别所有相关资产。
"""

ASSET_IDENTIFICATION_FROM_ARCHITECTURE_PROMPT = """你是一位汽车网络安全专家。请分析这张汽车电子架构图，识别其中的所有资产。

对于每个识别的资产，请提供：
1. 资产ID（如HW-001, SW-001等）
2. 资产名称
3. 资产分类（硬件/软件/数据/接口/外部实体）
4. 子分类
5. 资产描述
6. 安全属性（真实性、完整性、不可抵赖性、机密性、可用性、授权性）

同时，请识别资产之间的关系：
- 连接关系（如：ECU A 通过CAN总线连接到 ECU B）
- 包含关系（如：IVI系统包含多媒体应用）
- 依赖关系（如：导航功能依赖GPS模块）

请以JSON格式输出：

```json
{
  "assets": [...],
  "relations": [
    {
      "source": "HW-001",
      "target": "HW-002",
      "relation_type": "connects_to",
      "protocol": "CAN",
      "description": "通过CAN总线通信"
    }
  ]
}
```
"""
