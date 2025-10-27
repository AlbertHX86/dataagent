"""
数据模型定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DataFormat(str, Enum):
    """支持的数据格式"""
    CSV = "csv"
    JSON = "json"
    TXT = "txt"

class AnalysisRequest(BaseModel):
    """分析请求模型"""
    dataset_id: str = Field(..., description="数据集ID")
    user_query: str = Field(..., description="用户自然语言需求")
    data_description: Optional[str] = Field(None, description="数据描述")

class PredictionRequest(BaseModel):
    """预测请求模型"""
    dataset_id: str = Field(..., description="数据集ID")
    target_column: str = Field(..., description="目标预测列")
    prediction_query: str = Field(..., description="预测需求描述")
    model_type: Optional[str] = Field(None, description="模型类型")
    forecast_periods: Optional[int] = Field(10, description="预测周期数")

class DatasetInfo(BaseModel):
    """数据集信息"""
    id: str
    filename: str
    format: DataFormat
    upload_time: datetime
    rows: int
    columns: int
    column_names: List[str]
    data_types: Dict[str, str]
    description: Optional[str] = None

class ChartConfig(BaseModel):
    """图表配置"""
    type: str = Field(..., description="图表类型")
    title: str = Field(..., description="图表标题")
    data: Dict[str, Any] = Field(..., description="图表数据")
    config: Optional[Dict[str, Any]] = Field({}, description="额外配置")

class AnalysisResult(BaseModel):
    """分析结果"""
    analysis_id: str
    dataset_id: str
    summary: str = Field(..., description="分析摘要")
    insights: List[str] = Field(..., description="关键洞察")
    charts: List[ChartConfig] = Field(..., description="生成的图表")
    statistics: Dict[str, Any] = Field(..., description="统计数据")
    created_at: datetime

class PredictionResult(BaseModel):
    """预测结果"""
    prediction_id: str
    dataset_id: str
    model_name: str
    predictions: List[float]
    confidence_intervals: Optional[List[Dict[str, float]]] = None
    metrics: Dict[str, float]
    validation_passed: bool
    validation_details: Dict[str, Any]
    chart: ChartConfig
    created_at: datetime

class WorkRecord(BaseModel):
    """工作记录卡片"""
    record_id: str
    user_id: str
    title: str
    type: str  # "analysis" or "prediction"
    dataset_name: str
    description: str
    thumbnail: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    result_id: str

class UserInfo(BaseModel):
    """用户信息"""
    user_id: str
    username: str
    email: Optional[str] = None
    created_at: datetime
    work_records: List[WorkRecord] = []

class ErrorResponse(BaseModel):
    """错误响应"""
    error: str
    detail: Optional[str] = None

