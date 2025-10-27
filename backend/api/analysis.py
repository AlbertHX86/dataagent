"""
数据分析API
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
from datetime import datetime
import json
import os

from models.schemas import AnalysisRequest, AnalysisResult, ChartConfig
from services.analyzer import DataAnalyzer
from services.ai_service import AIService

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_data(request: AnalysisRequest):
    """
    执行数据分析
    
    根据用户的自然语言需求，自动分析数据并生成可视化结果
    """
    try:
        # 验证数据集存在
        metadata_path = f"uploads/datasets/{request.dataset_id}_metadata.json"
        if not os.path.exists(metadata_path):
            raise HTTPException(
                status_code=404,
                detail="数据集不存在"
            )
        
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        # 初始化分析器
        analyzer = DataAnalyzer(metadata["file_path"], metadata["format"])
        ai_service = AIService()
        
        # 加载数据
        df = analyzer.load_data()
        
        # 使用AI理解用户需求
        analysis_plan = await ai_service.generate_analysis_plan(
            user_query=request.user_query,
            data_description=request.data_description or "",
            column_names=metadata["column_names"],
            data_types=metadata["data_types"]
        )
        
        # 执行基础统计分析
        statistics = analyzer.get_basic_statistics()
        
        # 根据分析计划生成图表
        charts = []
        
        # 1. 数据分布图
        if analysis_plan.get("include_distribution", True):
            dist_charts = analyzer.create_distribution_charts()
            charts.extend(dist_charts)
        
        # 2. 相关性分析
        if analysis_plan.get("include_correlation", True) and analyzer.has_numeric_columns():
            corr_chart = analyzer.create_correlation_heatmap()
            if corr_chart:
                charts.append(corr_chart)
        
        # 3. 趋势分析
        if analysis_plan.get("include_trends", False):
            trend_charts = analyzer.create_trend_charts()
            charts.extend(trend_charts)
        
        # 4. 分类分析
        if analysis_plan.get("include_categories", True):
            cat_charts = analyzer.create_categorical_charts()
            charts.extend(cat_charts)
        
        # 使用AI生成分析摘要和洞察
        summary, insights = await ai_service.generate_insights(
            statistics=statistics,
            data_description=request.data_description or "",
            user_query=request.user_query,
            column_info=metadata
        )
        
        # 生成分析ID
        analysis_id = str(uuid.uuid4())
        
        # 保存分析结果
        result = AnalysisResult(
            analysis_id=analysis_id,
            dataset_id=request.dataset_id,
            summary=summary,
            insights=insights,
            charts=charts,
            statistics=statistics,
            created_at=datetime.now()
        )
        
        # 保存到文件
        result_path = f"uploads/results/{analysis_id}_analysis.json"
        os.makedirs("uploads/results", exist_ok=True)
        
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result.model_dump(mode='json'), f, ensure_ascii=False, indent=2, default=str)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"数据分析失败: {str(e)}"
        )

@router.get("/result/{analysis_id}", response_model=AnalysisResult)
async def get_analysis_result(analysis_id: str):
    """获取分析结果"""
    try:
        result_path = f"uploads/results/{analysis_id}_analysis.json"
        
        if not os.path.exists(result_path):
            raise HTTPException(
                status_code=404,
                detail="分析结果不存在"
            )
        
        with open(result_path, "r", encoding="utf-8") as f:
            result_data = json.load(f)
        
        return AnalysisResult(**result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取分析结果失败: {str(e)}"
        )

