# Instructions

## 需求生成

面向汽车行业的智能威胁分析与风险评估（TARA）平台，基于ISO/SAE 21434标准，结合AI智能体技术，实现汽车网络安全风险的自动化分析与评估。

输入包括架构图、功能清单、通信矩阵、接口定义、数据资产清单、安全需求文档、已有安全措施等，形式可能是任意文档（doc/excel/pdf等）、图片，支持导出excel格式的报告，格式需要严格和./docs/MY25EV_Platform_IVI_TARA_Report.xlsx格式保持一致，包含自动计算的列。

支持从文档中识别资产、构建资产关系知识图谱，存入neo4j。

包含项目管理、文档解析、资产识别、威胁风险分析、图表生成、报告中心、智能体服务、知识库服务、通知服务等模块，支持按项目生成报告，每个项目支持生成不同版本的报告。

OCR、多模态、语言、嵌入模型使用阿里云百炼平台 Qwen API 服务。

前端的设计风格请参考./docs/tara-ui.html。

技术栈如下：
前端: TypeScript, TailwindCSS, Vite
后端： python（UV），FastAPI, SQLAlchemy, Pydantic, Uvicorn
数据存储: MySQL 8.0, Redis 7, Neo4j 5, Milvus 2.3, ElasticSearch 8, MinIO
消息队列: Kafka
基础设施: Docker, Docker Compose, Nginx
构建工具: Make
开发与运行目标环境： x86_64 / Ubuntu 22+	

按照这个想法，帮我生成详细的需求和设计，放在./specs/0001-spec.md 文件中, 输出为中文。


## phase1