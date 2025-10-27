#!/bin/bash

# 数据分析Agent启动脚本

echo "========================================="
echo "  数据分析Agent - 启动脚本"
echo "========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3未安装"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: Node.js未安装"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo "✅ Node.js版本: $(node --version)"
echo ""

# 启动后端
echo "🚀 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f "venv/.installed" ]; then
    echo "📦 升级pip..."
    python -m pip install --upgrade pip
    echo "📦 安装Python依赖..."
    python -m pip install -r ../requirements.txt
    if [ $? -eq 0 ]; then
        touch venv/.installed
        echo "✅ 依赖安装成功"
    else
        echo "❌ 依赖安装失败，请检查错误信息"
        exit 1
    fi
fi

# 启动后端
echo "🌟 后端服务启动在: http://localhost:8000"
python main.py &
BACKEND_PID=$!

cd ..

# 启动前端
echo ""
echo "🚀 启动前端服务..."
cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装Node依赖..."
    npm install
fi

# 启动前端
echo "🌟 前端服务启动在: http://localhost:3000"
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================="
echo "  ✅ 服务启动成功！"
echo "========================================="
echo "  后端: http://localhost:8000"
echo "  前端: http://localhost:3000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "  按Ctrl+C退出所有服务"
echo "========================================="

# 等待用户中断
wait

