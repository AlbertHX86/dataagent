"""
预测服务 - 时间序列和机器学习预测
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import json
import plotly.graph_objects as go
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from models.schemas import ChartConfig

class TimeSeriesPredictor:
    """时间序列预测器"""
    
    def __init__(self, file_path: str, file_format: str):
        self.file_path = file_path
        self.file_format = file_format
        self.df = None
    
    def load_data(self) -> pd.DataFrame:
        """加载数据"""
        if self.file_format == 'csv':
            self.df = pd.read_csv(self.file_path)
        elif self.file_format == 'json':
            self.df = pd.read_json(self.file_path)
        elif self.file_format == 'txt':
            try:
                self.df = pd.read_csv(self.file_path, sep='\t')
            except:
                self.df = pd.read_csv(self.file_path, sep=',')
        
        return self.df
    
    def validate_assumptions(
        self,
        series: pd.Series,
        check_stationarity: bool = True,
        check_seasonality: bool = True,
        check_trend: bool = True
    ) -> Dict[str, Any]:
        """
        验证时间序列假设
        
        Args:
            series: 时间序列数据
            check_stationarity: 是否检查平稳性
            check_seasonality: 是否检查季节性
            check_trend: 是否检查趋势
        
        Returns:
            验证结果字典
        """
        result = {
            "is_valid": True,
            "tests": {},
            "recommendations": []
        }
        
        # 去除缺失值
        series_clean = series.dropna()
        
        if len(series_clean) < 10:
            result["is_valid"] = False
            result["recommendations"].append("数据量太少，至少需要10个数据点")
            return result
        
        # 1. 平稳性检验 (ADF Test)
        if check_stationarity:
            try:
                adf_result = adfuller(series_clean)
                result["tests"]["adf_test"] = {
                    "statistic": float(adf_result[0]),
                    "pvalue": float(adf_result[1]),
                    "is_stationary": adf_result[1] < 0.05
                }
                
                if not result["tests"]["adf_test"]["is_stationary"]:
                    result["recommendations"].append("数据非平稳，建议进行差分或对数变换")
            except Exception as e:
                result["tests"]["adf_test"] = {"error": str(e)}
        
        # 2. 趋势检测
        if check_trend:
            try:
                # 使用线性回归检测趋势
                x = np.arange(len(series_clean))
                coeffs = np.polyfit(x, series_clean.values, 1)
                
                result["tests"]["trend"] = {
                    "slope": float(coeffs[0]),
                    "has_trend": abs(coeffs[0]) > 0.01
                }
                
                if result["tests"]["trend"]["has_trend"]:
                    result["recommendations"].append("数据存在明显趋势")
            except Exception as e:
                result["tests"]["trend"] = {"error": str(e)}
        
        # 3. 季节性检测
        if check_seasonality and len(series_clean) >= 20:
            try:
                # 使用自相关函数检测季节性
                acf_values = acf(series_clean, nlags=min(20, len(series_clean) // 2))
                
                # 检查是否有显著的周期性峰值
                peaks = []
                for i in range(2, len(acf_values)):
                    if abs(acf_values[i]) > 0.3:  # 阈值
                        peaks.append(i)
                
                result["tests"]["seasonality"] = {
                    "has_seasonality": len(peaks) > 0,
                    "possible_periods": peaks[:3]  # 最多显示3个可能的周期
                }
                
                if result["tests"]["seasonality"]["has_seasonality"]:
                    result["recommendations"].append(
                        f"数据可能存在周期性，周期为: {peaks[:3]}"
                    )
            except Exception as e:
                result["tests"]["seasonality"] = {"error": str(e)}
        
        return result
    
    def transform_data(
        self,
        series: pd.Series,
        validation_result: Dict[str, Any]
    ) -> pd.Series:
        """
        根据验证结果转换数据
        """
        transformed = series.copy()
        
        # 如果非平稳，进行差分
        if "adf_test" in validation_result.get("tests", {}):
            if not validation_result["tests"]["adf_test"].get("is_stationary", True):
                transformed = transformed.diff().dropna()
        
        return transformed
    
    def select_best_model(
        self,
        series: pd.Series,
        validation_result: Dict[str, Any]
    ) -> str:
        """
        根据数据特征选择最佳模型
        """
        has_trend = validation_result.get("tests", {}).get("trend", {}).get("has_trend", False)
        has_seasonality = validation_result.get("tests", {}).get("seasonality", {}).get("has_seasonality", False)
        
        if has_seasonality:
            return "holtwinters"  # Holt-Winters指数平滑
        elif has_trend:
            return "arima"  # ARIMA
        else:
            return "exponential_smoothing"  # 简单指数平滑
    
    def predict(
        self,
        series: pd.Series,
        model_type: str = "arima",
        forecast_periods: int = 10
    ) -> Tuple[np.ndarray, Optional[List[Dict]], Dict[str, float]]:
        """
        执行预测
        
        Args:
            series: 时间序列数据
            model_type: 模型类型
            forecast_periods: 预测周期数
        
        Returns:
            (预测值, 置信区间, 评估指标)
        """
        series_clean = series.dropna()
        
        # 分割训练集和测试集
        train_size = int(len(series_clean) * 0.8)
        train = series_clean[:train_size]
        test = series_clean[train_size:]
        
        predictions = None
        confidence_intervals = None
        
        try:
            if model_type == "arima":
                predictions, confidence_intervals = self._predict_arima(
                    train, test, forecast_periods
                )
            elif model_type == "holtwinters":
                predictions, confidence_intervals = self._predict_holtwinters(
                    train, test, forecast_periods
                )
            elif model_type == "exponential_smoothing":
                predictions, confidence_intervals = self._predict_exponential_smoothing(
                    train, test, forecast_periods
                )
            else:
                # 默认使用ARIMA
                predictions, confidence_intervals = self._predict_arima(
                    train, test, forecast_periods
                )
        except Exception as e:
            # 如果模型失败，使用简单的移动平均作为后备
            window = min(5, len(train) // 2)
            last_values = train.tail(window).mean()
            predictions = np.array([last_values] * forecast_periods)
            confidence_intervals = None
        
        # 计算评估指标
        metrics = {}
        if len(test) > 0 and predictions is not None:
            test_predictions = predictions[:len(test)]
            metrics = {
                "mse": float(mean_squared_error(test, test_predictions)),
                "mae": float(mean_absolute_error(test, test_predictions)),
                "rmse": float(np.sqrt(mean_squared_error(test, test_predictions)))
            }
        
        return predictions, confidence_intervals, metrics
    
    def _predict_arima(
        self,
        train: pd.Series,
        test: pd.Series,
        forecast_periods: int
    ) -> Tuple[np.ndarray, List[Dict]]:
        """ARIMA预测"""
        # 使用自动选择的参数
        model = ARIMA(train, order=(1, 1, 1))
        model_fit = model.fit()
        
        # 预测
        forecast = model_fit.forecast(steps=forecast_periods)
        
        # 获取置信区间
        forecast_result = model_fit.get_forecast(steps=forecast_periods)
        conf_int = forecast_result.conf_int()
        
        confidence_intervals = [
            {
                "lower": float(conf_int.iloc[i, 0]),
                "upper": float(conf_int.iloc[i, 1])
            }
            for i in range(len(conf_int))
        ]
        
        return forecast.values, confidence_intervals
    
    def _predict_holtwinters(
        self,
        train: pd.Series,
        test: pd.Series,
        forecast_periods: int
    ) -> Tuple[np.ndarray, None]:
        """Holt-Winters指数平滑预测"""
        try:
            # 尝试使用季节性模型
            seasonal_periods = min(12, len(train) // 2)
            if seasonal_periods < 2:
                seasonal_periods = 2
            
            model = ExponentialSmoothing(
                train,
                seasonal_periods=seasonal_periods,
                trend='add',
                seasonal='add'
            )
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=forecast_periods)
            
            return forecast.values, None
        except:
            # 如果失败，使用简单指数平滑
            return self._predict_exponential_smoothing(train, test, forecast_periods)
    
    def _predict_exponential_smoothing(
        self,
        train: pd.Series,
        test: pd.Series,
        forecast_periods: int
    ) -> Tuple[np.ndarray, None]:
        """简单指数平滑预测"""
        model = ExponentialSmoothing(train, trend='add')
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_periods)
        
        return forecast.values, None
    
    def create_prediction_chart(
        self,
        actual_data: pd.Series,
        predictions: np.ndarray,
        confidence_intervals: Optional[List[Dict]],
        title: str = "Prediction Results"
    ) -> ChartConfig:
        """创建预测结果图表"""
        fig = go.Figure()
        
        # 实际数据
        fig.add_trace(go.Scatter(
            x=list(range(len(actual_data))),
            y=actual_data.values,
            mode='lines',
            name='Actual Data',
            line=dict(color='blue')
        ))
        
        # 预测数据
        prediction_x = list(range(len(actual_data), len(actual_data) + len(predictions)))
        fig.add_trace(go.Scatter(
            x=prediction_x,
            y=predictions,
            mode='lines',
            name='Predictions',
            line=dict(color='red', dash='dash')
        ))
        
        # 置信区间
        if confidence_intervals:
            upper = [ci["upper"] for ci in confidence_intervals]
            lower = [ci["lower"] for ci in confidence_intervals]
            
            fig.add_trace(go.Scatter(
                x=prediction_x + prediction_x[::-1],
                y=upper + lower[::-1],
                fill='toself',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval',
                showlegend=True
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Value',
            hovermode='x'
        )
        
        chart_data = json.loads(fig.to_json())
        
        return ChartConfig(
            type="prediction",
            title=title,
            data=chart_data,
            config={}
        )

