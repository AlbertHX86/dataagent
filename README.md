# 数据分析 Agent

一个智能数据分析Web应用，帮助用户轻松完成数据分析、可视化和预测任务。

## 功能特性

### 核心功能
- 📊 **智能数据分析**: 支持CSV、JSON、TXT等多种数据格式上传
- 📈 **自动可视化**: 自动生成多种统计图表和数据看板
- 🤖 **AI驱动**: 使用自然语言描述需求，AI自动完成分析任务
- 📉 **预测分析**: 支持时间序列预测和机器学习模型

### 高级功能
- 🔮 **智能预测**: 自动验证数据假设，选择最佳预测模型
- 🎨 **自定义分析**: 通过自然语言定义复杂分析流程
- 💾 **工作记录**: 保存和管理所有分析历史
- 👤 **用户系统**: 个人工作空间和数据管理

## 技术栈

### 后端
- **FastAPI**: 高性能Web框架
- **Pandas**: 数据处理和分析
- **NumPy**: 数值计算
- **Matplotlib/Plotly**: 数据可视化
- **Scikit-learn**: 机器学习
- **Statsmodels**: 统计模型和时间序列分析
- **OpenAI API**: AI自然语言处理

### 前端
- **React**: UI框架
- **TypeScript**: 类型安全
- **Ant Design**: UI组件库
- **Recharts/Plotly.js**: 图表库
- **Axios**: HTTP客户端
- **React Router**: 路由管理

## 项目结构

```
DSagent/
├── backend/              # 后端代码
│   ├── api/             # API路由
│   ├── core/            # 核心功能
│   ├── models/          # 数据模型
│   ├── services/        # 业务逻辑
│   └── main.py          # 应用入口
├── frontend/            # 前端代码
│   ├── src/
│   │   ├── components/  # React组件
│   │   ├── pages/       # 页面
│   │   ├── services/    # API服务
│   │   └── App.tsx      # 应用入口
│   └── package.json
└── requirements.txt     # Python依赖
```

## 快速开始

### 后端启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端服务
cd backend
python main.py
```

后端将运行在 http://localhost:8000

### 前端启动

```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器
npm start
```

前端将运行在 http://localhost:3000

## 使用指南

1. **上传数据**: 在首页上传CSV、JSON或TXT格式的数据文件
2. **描述需求**: 用自然语言描述你的数据和分析需求
3. **查看分析**: 系统自动生成数据看板和可视化图表
4. **高级功能**: 使用预测功能进行时间序列分析或机器学习预测
5. **保存工作**: 所有分析结果自动保存到工作记录

## 环境变量

创建 `.env` 文件在项目根目录：

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## License

MIT

