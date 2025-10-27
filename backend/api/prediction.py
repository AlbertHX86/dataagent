"""
预测功能API
"""
from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime
import json
import os

from models.schemas import PredictionRequest, PredictionResult, ChartConfig
from services.predictor import TimeSeriesPredictor
from services.ai_service import AIService

router = APIRouter()

@router.post("/predict", response_model=PredictionResult)
async def predict_data(request: PredictionRequest):
    """
    执行预测分析
    
    支持时间序列预测和机器学习模型预测
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
        
        # 初始化预测器
        predictor = TimeSeriesPredictor(metadata["file_path"], metadata["format"])
        ai_service = AIService()
        
        # 加载数据
        df = predictor.load_data()
        
        # 验证目标列存在
        if request.target_column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"目标列 '{request.target_column}' 不存在"
            )
        
        # 使用AI理解预测需求
        prediction_config = await ai_service.generate_prediction_config(
            prediction_query=request.prediction_query,
            target_column=request.target_column,
            column_names=metadata["column_names"],
            data_types=metadata["data_types"]
        )
        
        # 验证数据假设
        validation_result = predictor.validate_assumptions(
            df[request.target_column],
            check_stationarity=True,
            check_seasonality=True,
            check_trend=True
        )
        
        if not validation_result["is_valid"]:
            # 如果不满足假设，尝试转换数据
            df[request.target_column] = predictor.transform_data(
                df[request.target_column],
                validation_result
            )
            
            # 重新验证
            validation_result = predictor.validate_assumptions(
                df[request.target_column],
                check_stationarity=True,
                check_seasonality=True,
                check_trend=True
            )
        
        # 选择最佳模型
        if not request.model_type:
            model_type = predictor.select_best_model(
                df[request.target_column],
                validation_result
            )
        else:
            model_type = request.model_type
        
        # 执行预测
        predictions, confidence_intervals, metrics = predictor.predict(
            df[request.target_column],
            model_type=model_type,
            forecast_periods=request.forecast_periods
        )
        
        # 创建预测图表
        chart = predictor.create_prediction_chart(
            actual_data=df[request.target_column],
            predictions=predictions,
            confidence_intervals=confidence_intervals,
            title=f"{request.target_column} Prediction"
        )
        
        # 生成预测ID
        prediction_id = str(uuid.uuid4())
        
        # 保存预测结果
        result = PredictionResult(
            prediction_id=prediction_id,
            dataset_id=request.dataset_id,
            model_name=model_type,
            predictions=predictions.tolist() if hasattr(predictions, 'tolist') else predictions,
            confidence_intervals=confidence_intervals,
            metrics=metrics,
            validation_passed=validation_result["is_valid"],
            validation_details=validation_result,
            chart=chart,
            created_at=datetime.now()
        )
        
        # 保存到文件
        result_path = f"uploads/results/{prediction_id}_prediction.json"
        os.makedirs("uploads/results", exist_ok=True)
        
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result.model_dump(mode='json'), f, ensure_ascii=False, indent=2, default=str)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"预测分析失败: {str(e)}"
        )

@router.get("/result/{prediction_id}", response_model=PredictionResult)
async def get_prediction_result(prediction_id: str):
    """获取预测结果"""
    try:
        result_path = f"uploads/results/{prediction_id}_prediction.json"
        
        if not os.path.exists(result_path):
            raise HTTPException(
                status_code=404,
                detail="预测结果不存在"
            )
        
        with open(result_path, "r", encoding="utf-8") as f:
            result_data = json.load(f)
        
        return PredictionResult(**result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取预测结果失败: {str(e)}"
        )

@router.post("/validate/{dataset_id}")
async def validate_time_series(dataset_id: str, column: str):
    """
    验证数据是否满足时间序列假设
    """
    try:
        metadata_path = f"uploads/datasets/{dataset_id}_metadata.json"
        if not os.path.exists(metadata_path):
            raise HTTPException(
                status_code=404,
                detail="数据集不存在"
            )
        
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        predictor = TimeSeriesPredictor(metadata["file_path"], metadata["format"])
        df = predictor.load_data()
        
        if column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"列 '{column}' 不存在"
            )
        
        validation_result = predictor.validate_assumptions(
            df[column],
            check_stationarity=True,
            check_seasonality=True,
            check_trend=True
        )
        
        return validation_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"验证失败: {str(e)}"
        )

