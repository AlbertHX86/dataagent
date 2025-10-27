# 安装指南

## 方法一：手动安装（推荐）

### 1. 后端安装

```bash
cd /Users/albert/Desktop/DSagent/backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip
python -m pip install --upgrade pip

# 安装依赖
python -m pip install -r ../requirements.txt
```

### 2. 前端安装

打开**新的终端窗口**：

```bash
cd /Users/albert/Desktop/DSagent/frontend

# 安装依赖
npm install
```

## 启动服务

### 启动后端

在后端终端（确保虚拟环境已激活）：

```bash
cd /Users/albert/Desktop/DSagent/backend
source venv/bin/activate  # 如果环境未激活
python main.py
```

后端将运行在: **http://localhost:8000**

### 启动前端

在前端终端（新窗口）：

```bash
cd /Users/albert/Desktop/DSagent/frontend
npm start
```

前端将运行在: **http://localhost:3000**

浏览器会自动打开，或者手动访问: http://localhost:3000

## 方法二：使用启动脚本

如果你想使用启动脚本，需要手动先安装依赖：

```bash
# 1. 先手动安装后端依赖（按方法一的步骤）
cd backend
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ../requirements.txt

# 2. 创建标记文件
touch venv/.installed

# 3. 退出当前目录
cd ..

# 4. 运行启动脚本
./start.sh
```

## 验证安装

### 检查后端

访问: http://localhost:8000

应该看到:
```json
{
  "message": "欢迎使用数据分析Agent API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

访问API文档: http://localhost:8000/docs

### 检查前端

访问: http://localhost:3000

应该看到数据分析Agent的首页

## 常见问题

### Q: pip安装失败？

**A**: 确保：
1. 虚拟环境已激活 (命令提示符前有`(venv)`)
2. 使用 `python -m pip` 而不是直接 `pip`
3. 检查网络连接

### Q: 前端npm install失败？

**A**: 尝试：
```bash
# 清理缓存
npm cache clean --force

# 删除node_modules
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### Q: 端口被占用？

**A**: 修改端口：

后端 - 在 `.env` 文件中：
```env
PORT=8001  # 改为其他端口
```

前端 - 设置环境变量：
```bash
PORT=3001 npm start
```

### Q: 找不到某个Python模块？

**A**: 确保：
1. 虚拟环境已激活
2. 在backend目录运行python
3. 所有依赖都已安装成功

## 卸载

```bash
# 删除后端虚拟环境
rm -rf backend/venv

# 删除前端依赖
rm -rf frontend/node_modules

# 删除上传的文件
rm -rf uploads/
```

## 下一步

安装成功后，查看 [QUICK_START.md](QUICK_START.md) 了解如何使用系统。

---

如有问题，请检查：
1. Python版本 >= 3.8
2. Node.js版本 >= 14
3. 网络连接正常
4. 磁盘空间充足

