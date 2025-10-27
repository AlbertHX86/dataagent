# 快速开始指南

## 系统要求

- Python 3.8+
- Node.js 14+
- npm 或 yarn

## 快速启动

### 方式一：使用启动脚本（推荐）

```bash
# 1. 克隆或进入项目目录
cd DSagent

# 2. 添加执行权限
chmod +x start.sh

# 3. 运行启动脚本
./start.sh
```

启动脚本会自动：
- 创建Python虚拟环境
- 安装所有依赖
- 启动后端和前端服务

### 方式二：手动启动

#### 1. 启动后端

```bash
# 创建虚拟环境
python3 -m venv backend/venv

# 激活虚拟环境
source backend/venv/bin/activate  # Linux/Mac
# 或
backend\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动后端
cd backend
python main.py
```

后端将运行在: http://localhost:8000

#### 2. 启动前端

打开新终端：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动前端
npm start
```

前端将运行在: http://localhost:3000

## 配置

### 后端配置

在项目根目录创建 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
DEBUG=True
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000
```

> **注意**: OpenAI API Key 是可选的。如果不配置，系统会使用默认的分析逻辑，但不会有AI增强的自然语言处理功能。

### 前端配置

在 `frontend` 目录创建 `.env` 文件：

```env
REACT_APP_API_URL=http://localhost:8000
```

## 使用流程

1. **访问应用**: 打开浏览器访问 http://localhost:3000
2. **登录**: 点击"登录"按钮（演示版本可直接进入）
3. **上传数据**: 在首页上传CSV/JSON/TXT格式的数据文件
4. **数据分析**: 
   - 用自然语言描述分析需求
   - 查看自动生成的图表和洞察
5. **预测分析**:
   - 选择目标预测列
   - 验证数据假设
   - 执行预测并查看结果
6. **查看历史**: 在"我的工作"页面查看所有分析记录

## 测试数据

项目没有包含测试数据集。您可以使用自己的数据，或创建简单的CSV文件进行测试：

```csv
date,sales,revenue
2023-01-01,100,1000
2023-01-02,120,1200
2023-01-03,95,950
2023-01-04,130,1300
2023-01-05,110,1100
```

## 常见问题

### Q: 后端启动失败？
A: 检查Python版本是否>=3.8，确保所有依赖已安装

### Q: 前端无法连接后端？
A: 确保后端正在运行，检查`.env`文件中的API_URL配置

### Q: AI功能不工作？
A: 需要配置OpenAI API Key。如果不配置，系统会使用基础分析功能

### Q: 上传文件失败？
A: 检查文件格式（仅支持CSV、JSON、TXT），文件大小需<100MB

## 获取帮助

- 查看完整文档: `README.md`
- API文档: http://localhost:8000/docs
- 问题反馈: 创建GitHub Issue

## 停止服务

如果使用启动脚本：按 `Ctrl+C`

如果手动启动：在各自的终端窗口按 `Ctrl+C`

