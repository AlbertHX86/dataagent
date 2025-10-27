# 立即启动指南

## ✅ 后端依赖已安装成功！

现在按照以下步骤启动服务：

## 步骤 1: 启动后端

打开终端，运行：

```bash
cd /Users/albert/Desktop/DSagent/backend
source venv/bin/activate
python main.py
```

你应该看到类似的输出：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**保持这个终端窗口开启**

## 步骤 2: 启动前端

**打开新的终端窗口**，运行：

```bash
cd /Users/albert/Desktop/DSagent/frontend
npm install
npm start
```

第一次运行需要安装依赖（可能需要2-3分钟）

前端启动后，浏览器会自动打开 http://localhost:3000

## 步骤 3: 开始使用

1. 点击"登录"按钮（演示版可以直接进入）
2. 上传 `example_data.csv` 文件测试
3. 输入分析需求，例如：
   - "分析销售数据的趋势和分布"
   - "找出收入和客户数的关系"
4. 查看自动生成的图表和洞察！

## 访问地址

- 🌐 前端应用: http://localhost:3000
- 🔧 后端API: http://localhost:8000
- 📚 API文档: http://localhost:8000/docs

## 停止服务

在各自的终端窗口按 `Ctrl+C`

## 遇到问题？

### 前端npm install失败？
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### 端口被占用？
后端换端口：
```bash
PORT=8001 python main.py
```

前端换端口：
```bash
PORT=3001 npm start
```

---

🎉 **现在就开始吧！**

