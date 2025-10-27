"""
数据分析服务
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
import json

from models.schemas import ChartConfig

class DataAnalyzer:
    """数据分析器"""
    
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
    
    def get_basic_statistics(self) -> Dict[str, Any]:
        """获取基础统计信息"""
        if self.df is None:
            self.load_data()
        
        stats = {
            "shape": {
                "rows": int(self.df.shape[0]),
                "columns": int(self.df.shape[1])
            },
            "columns": {},
            "missing_values": {},
            "data_types": {}
        }
        
        # 数值列统计
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols:
            stats["columns"][col] = {
                "mean": float(self.df[col].mean()),
                "median": float(self.df[col].median()),
                "std": float(self.df[col].std()),
                "min": float(self.df[col].min()),
                "max": float(self.df[col].max()),
                "q25": float(self.df[col].quantile(0.25)),
                "q75": float(self.df[col].quantile(0.75))
            }
            stats["missing_values"][col] = int(self.df[col].isna().sum())
            stats["data_types"][col] = "numeric"
        
        # 分类列统计
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        for col in categorical_cols:
            value_counts = self.df[col].value_counts()
            stats["columns"][col] = {
                "unique_values": int(self.df[col].nunique()),
                "most_common": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                "most_common_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
            }
            stats["missing_values"][col] = int(self.df[col].isna().sum())
            stats["data_types"][col] = "categorical"
        
        return stats
    
    def has_numeric_columns(self) -> bool:
        """检查是否有数值列"""
        if self.df is None:
            self.load_data()
        return len(self.df.select_dtypes(include=[np.number]).columns) > 0
    
    def create_distribution_charts(self) -> List[ChartConfig]:
        """创建分布图表"""
        if self.df is None:
            self.load_data()
        
        charts = []
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 限制最多显示5个数值列的分布
        for col in numeric_cols[:5]:
            # 使用Plotly创建直方图
            fig = px.histogram(
                self.df,
                x=col,
                title=f"Distribution of {col}",
                nbins=30
            )
            
            chart_data = json.loads(fig.to_json())
            
            charts.append(ChartConfig(
                type="histogram",
                title=f"{col} Distribution",
                data=chart_data,
                config={"column": col}
            ))
        
        return charts
    
    def create_correlation_heatmap(self) -> Optional[ChartConfig]:
        """创建相关性热力图"""
        if self.df is None:
            self.load_data()
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return None
        
        # 计算相关系数
        corr_matrix = numeric_df.corr()
        
        # 使用Plotly创建热力图
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale='RdBu',
            zmid=0
        ))
        
        fig.update_layout(
            title="Correlation Heatmap",
            xaxis_title="Variables",
            yaxis_title="Variables"
        )
        
        chart_data = json.loads(fig.to_json())
        
        return ChartConfig(
            type="heatmap",
            title="Correlation Analysis",
            data=chart_data,
            config={"correlation_matrix": corr_matrix.to_dict()}
        )
    
    def create_trend_charts(self) -> List[ChartConfig]:
        """创建趋势图表"""
        if self.df is None:
            self.load_data()
        
        charts = []
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 如果数据有索引列或时间列，创建趋势图
        if len(numeric_cols) > 0:
            # 限制最多3个趋势图
            for col in numeric_cols[:3]:
                fig = px.line(
                    self.df,
                    y=col,
                    title=f"Trend of {col}"
                )
                
                chart_data = json.loads(fig.to_json())
                
                charts.append(ChartConfig(
                    type="line",
                    title=f"{col} Trend",
                    data=chart_data,
                    config={"column": col}
                ))
        
        return charts
    
    def create_categorical_charts(self) -> List[ChartConfig]:
        """创建分类图表"""
        if self.df is None:
            self.load_data()
        
        charts = []
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        
        # 限制最多显示3个分类列
        for col in categorical_cols[:3]:
            value_counts = self.df[col].value_counts().head(10)
            
            # 使用Plotly创建条形图
            fig = px.bar(
                x=value_counts.index.tolist(),
                y=value_counts.values.tolist(),
                title=f"Distribution of {col}",
                labels={'x': col, 'y': 'Count'}
            )
            
            chart_data = json.loads(fig.to_json())
            
            charts.append(ChartConfig(
                type="bar",
                title=f"{col} Distribution",
                data=chart_data,
                config={"column": col}
            ))
        
        return charts
    
    def create_scatter_matrix(self) -> Optional[ChartConfig]:
        """创建散点图矩阵"""
        if self.df is None:
            self.load_data()
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return None
        
        # 限制最多4个变量
        cols = numeric_df.columns[:4].tolist()
        
        fig = px.scatter_matrix(
            numeric_df[cols],
            title="Scatter Matrix"
        )
        
        chart_data = json.loads(fig.to_json())
        
        return ChartConfig(
            type="scatter_matrix",
            title="Variable Relationships",
            data=chart_data,
            config={"columns": cols}
        )

