# 系统架构

## 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                        前端层                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │        React + TypeScript + Ant Design           │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐│   │
│  │  │  首页  │  │ 分析页 │  │ 预测页 │  │工作区 ││   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘│   │
│  │  ┌────────────────────────────────────────────┐ │   │
│  │  │          API Service Layer                 │ │   │
│  │  └────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                      HTTP/REST API
                           │
┌─────────────────────────────────────────────────────────┐
│                        后端层                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │              FastAPI Framework                   │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐│   │
│  │  │Upload  │  │Analysis│  │Predict │  │ User  ││   │
│  │  │  API   │  │  API   │  │  API   │  │  API  ││   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘│   │
│  └──────────────────────────────────────────────────┘   │
│                           │                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Service Layer                       │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐             │   │
│  │  │Analyzer│  │Predictor│ │AI Service│            │   │
│  │  └────────┘  └────────┘  └────────┘             │   │
│  └──────────────────────────────────────────────────┘   │
│                           │                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Data Layer                          │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐             │   │
│  │  │ Pandas │  │ NumPy  │  │Plotly  │             │   │
│  │  └────────┘  └────────┘  └────────┘             │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
           ┌────────┴────┐  ┌────┴────────┐
           │ File Storage│  │ OpenAI API  │
           └─────────────┘  └─────────────┘
```

## 前端架构

### 技术栈
- **框架**: React 18 + TypeScript
- **UI库**: Ant Design 5
- **路由**: React Router 6
- **图表**: Plotly.js + Recharts
- **HTTP**: Axios
- **状态管理**: React Hooks (useState, useEffect)

### 目录结构
```
frontend/
├── public/
│   └── index.html           # HTML模板
├── src/
│   ├── components/          # 可复用组件
│   │   ├── Layout.tsx       # 页面布局
│   │   ├── DataUploader.tsx # 数据上传组件
│   │   └── ChartRenderer.tsx# 图表渲染组件
│   ├── pages/               # 页面组件
│   │   ├── HomePage.tsx     # 首页
│   │   ├── AnalysisPage.tsx # 分析页
│   │   ├── PredictionPage.tsx# 预测页
│   │   ├── WorkspacePage.tsx# 工作区
│   │   └── LoginPage.tsx    # 登录页
│   ├── services/            # API服务
│   │   └── api.ts           # API封装
│   ├── App.tsx              # 应用入口
│   └── index.tsx            # 渲染入口
├── package.json
└── tsconfig.json
```

### 组件设计原则
1. **单一职责**: 每个组件只负责一个功能
2. **可复用**: 通过props传递配置，提高复用性
3. **类型安全**: 使用TypeScript确保类型正确
4. **响应式**: 适配不同屏幕尺寸

## 后端架构

### 技术栈
- **框架**: FastAPI
- **数据处理**: Pandas, NumPy
- **可视化**: Matplotlib, Plotly
- **机器学习**: Scikit-learn, Statsmodels
- **AI**: OpenAI API
- **异步**: Asyncio

### 目录结构
```
backend/
├── api/                     # API路由层
│   ├── upload.py            # 数据上传API
│   ├── analysis.py          # 分析API
│   ├── prediction.py        # 预测API
│   └── user.py              # 用户API
├── models/                  # 数据模型
│   └── schemas.py           # Pydantic模型
├── services/                # 业务逻辑层
│   ├── analyzer.py          # 数据分析服务
│   ├── predictor.py         # 预测服务
│   └── ai_service.py        # AI服务
└── main.py                  # 应用入口
```

### 分层架构

#### 1. API层 (api/)
- 接收HTTP请求
- 参数验证
- 调用Service层
- 返回响应

#### 2. Service层 (services/)
- 业务逻辑处理
- 数据分析和预测
- AI集成
- 错误处理

#### 3. Model层 (models/)
- 数据模型定义
- 请求/响应格式
- 类型验证

## 数据流

### 数据上传流程
```
1. 用户选择文件
   ↓
2. 前端验证（格式、大小）
   ↓
3. FormData上传到后端
   ↓
4. 后端保存文件
   ↓
5. 解析数据，提取元信息
   ↓
6. 保存元数据JSON
   ↓
7. 返回数据集信息给前端
```

### 数据分析流程
```
1. 用户输入分析需求
   ↓
2. 前端发送请求（dataset_id + query）
   ↓
3. 后端加载数据集
   ↓
4. AI解析用户需求，生成分析计划
   ↓
5. 执行数据分析
   │  ├─ 基础统计
   │  ├─ 数据分布
   │  ├─ 相关性分析
   │  └─ 趋势分析
   ↓
6. 生成可视化图表
   ↓
7. AI生成摘要和洞察
   ↓
8. 保存分析结果
   ↓
9. 返回结果给前端
```

### 预测流程
```
1. 用户选择目标列
   ↓
2. 验证数据假设
   │  ├─ 平稳性检验
   │  ├─ 趋势检测
   │  └─ 季节性检测
   ↓
3. 数据转换（如需要）
   ↓
4. 模型选择
   │  ├─ ARIMA
   │  ├─ Holt-Winters
   │  └─ 指数平滑
   ↓
5. 模型训练
   ↓
6. 执行预测
   ↓
7. 计算置信区间
   ↓
8. 评估模型性能
   ↓
9. 生成预测图表
   ↓
10. 保存预测结果
   ↓
11. 返回结果给前端
```

## API设计

### RESTful规范

```
资源              HTTP方法    路径                      描述
──────────────────────────────────────────────────────────
数据集            POST        /api/upload/dataset       上传数据集
数据集信息        GET         /api/upload/dataset/:id   获取数据集信息
数据预览          GET         /api/upload/dataset/:id/preview  预览数据

数据分析          POST        /api/analysis/analyze     执行分析
分析结果          GET         /api/analysis/result/:id  获取分析结果

预测              POST        /api/prediction/predict   执行预测
预测结果          GET         /api/prediction/result/:id 获取预测结果
数据验证          POST        /api/prediction/validate/:id 验证数据

用户注册          POST        /api/user/register        用户注册
用户信息          GET         /api/user/info/:id        获取用户信息
工作记录          GET         /api/user/records/:id     获取工作记录
添加记录          POST        /api/user/records/:id     添加工作记录
删除记录          DELETE      /api/user/records/:id/:rid 删除工作记录
```

### 响应格式

成功响应：
```json
{
  "data": {...},
  "message": "success"
}
```

错误响应：
```json
{
  "error": "ErrorType",
  "detail": "详细错误信息"
}
```

## 数据存储

### 文件系统结构
```
uploads/
├── datasets/                # 数据集文件
│   ├── {uuid}.csv
│   ├── {uuid}.json
│   ├── {uuid}_metadata.json # 元数据
│   └── ...
├── results/                 # 分析/预测结果
│   ├── {uuid}_analysis.json
│   ├── {uuid}_prediction.json
│   └── ...
└── users.json              # 用户数据（演示用）
```

### 元数据格式

数据集元数据：
```json
{
  "id": "uuid",
  "filename": "data.csv",
  "format": "csv",
  "upload_time": "2024-01-01T00:00:00",
  "rows": 1000,
  "columns": 10,
  "column_names": ["col1", "col2", ...],
  "data_types": {"col1": "int64", "col2": "float64"},
  "description": "数据描述",
  "file_path": "uploads/datasets/uuid.csv"
}
```

## AI集成

### OpenAI API使用

#### 分析计划生成
```
输入: 用户查询 + 数据信息
输出: 分析计划JSON
{
  "include_distribution": true,
  "include_correlation": true,
  "include_trends": true,
  "focus_columns": ["col1", "col2"]
}
```

#### 洞察生成
```
输入: 统计结果 + 用户查询
输出: 摘要 + 洞察列表
{
  "summary": "数据摘要...",
  "insights": ["洞察1", "洞察2", ...]
}
```

#### 预测配置
```
输入: 预测需求 + 数据信息
输出: 预测配置
{
  "model_type": "arima",
  "forecast_periods": 10,
  "include_confidence_interval": true
}
```

### 降级策略

如果AI服务不可用：
- 使用默认分析计划
- 返回基础统计摘要
- 使用启发式模型选择

## 安全设计

### 输入验证
- 文件类型白名单
- 文件大小限制
- SQL注入防护
- XSS防护

### 认证授权
- JWT token（未来实现）
- Session管理
- 权限控制

### 数据隔离
- 用户数据分离
- 临时文件清理
- 敏感信息脱敏

## 性能优化

### 后端优化
1. **异步处理**: 使用async/await处理IO操作
2. **缓存**: 缓存分析结果
3. **数据采样**: 大数据集先采样预览
4. **惰性加载**: 按需加载数据

### 前端优化
1. **代码分割**: 按路由分割代码
2. **懒加载**: 图表按需加载
3. **虚拟化**: 长列表虚拟滚动
4. **防抖节流**: 优化输入响应

### 网络优化
1. **请求合并**: 减少HTTP请求
2. **压缩**: Gzip压缩响应
3. **CDN**: 静态资源CDN加速
4. **HTTP/2**: 支持多路复用

## 可扩展性

### 水平扩展
- 无状态设计
- 负载均衡
- 分布式存储

### 垂直扩展
- 增加CPU/内存
- GPU加速计算
- 数据库优化

### 功能扩展
- 插件系统
- 自定义分析器
- 第三方集成

## 监控和日志

### 日志记录
- 访问日志
- 错误日志
- 性能日志
- 审计日志

### 监控指标
- 请求量/响应时间
- 错误率
- 资源使用率
- 用户活跃度

### 告警机制
- 错误率过高
- 响应时间超时
- 资源耗尽
- 服务宕机

## 部署架构

### 开发环境
```
本地开发 → 本地测试 → Git提交
```

### 生产环境
```
代码仓库 → CI/CD → Docker构建 → 容器部署 → 负载均衡
```

### 容器化
```dockerfile
# 后端Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "main.py"]

# 前端Dockerfile
FROM node:18
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
```

## 技术选型理由

### 为什么选择FastAPI？
- 高性能（基于Starlette和Pydantic）
- 自动生成API文档
- 原生支持异步
- 类型提示支持

### 为什么选择React？
- 组件化开发
- 强大的生态系统
- 虚拟DOM性能优异
- TypeScript集成良好

### 为什么选择Ant Design？
- 企业级UI设计
- 组件丰富完整
- 定制主题方便
- 中文文档完善

### 为什么选择Plotly？
- 交互式图表
- 丰富的图表类型
- 科学计算友好
- 导出功能强大

