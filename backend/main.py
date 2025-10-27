"""
数据分析Agent - 后端主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

from api import upload, analysis, prediction, user

# 加载环境变量
load_dotenv()  # 先加载.env
load_dotenv('.env.local')  # 再加载.env.local（会覆盖.env中的同名变量）

# 创建FastAPI应用
app = FastAPI(
    title="数据分析Agent API",
    description="智能数据分析和预测API",
    version="1.0.0"
)

# CORS配置
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/datasets", exist_ok=True)
os.makedirs("uploads/results", exist_ok=True)

# 注册路由
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(user.router, prefix="/api/user", tags=["User"])

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "欢迎使用数据分析Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )

