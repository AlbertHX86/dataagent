"""
AI服务 - 使用OpenAI API处理自然语言
"""
import os
from typing import Dict, Any, List, Tuple
import json
from openai import OpenAI

class AIService:
    """AI服务类"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
    
    async def generate_analysis_plan(
        self,
        user_query: str,
        data_description: str,
        column_names: List[str],
        data_types: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        根据用户查询生成分析计划
        """
        if not self.enabled:
            # 如果没有API key，返回默认计划
            return {
                "include_distribution": True,
                "include_correlation": True,
                "include_trends": True,
                "include_categories": True
            }
        
        prompt = f"""
        用户想要分析以下数据：
        
        数据描述：{data_description}
        
        列名和类型：
        {json.dumps({"columns": column_names, "types": data_types}, ensure_ascii=False, indent=2)}
        
        用户需求：{user_query}
        
        请根据用户需求，生成一个分析计划。返回JSON格式，包含以下字段：
        - include_distribution: 是否包含数据分布分析（布尔值）
        - include_correlation: 是否包含相关性分析（布尔值）
        - include_trends: 是否包含趋势分析（布尔值）
        - include_categories: 是否包含分类统计（布尔值）
        - focus_columns: 重点分析的列名列表
        - analysis_type: 分析类型（descriptive/diagnostic/predictive）
        
        只返回JSON，不要其他文字。
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的数据分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            plan = json.loads(content)
            return plan
        except Exception as e:
            # 如果AI调用失败，返回默认计划
            return {
                "include_distribution": True,
                "include_correlation": True,
                "include_trends": True,
                "include_categories": True
            }
    
    async def generate_insights(
        self,
        statistics: Dict[str, Any],
        data_description: str,
        user_query: str,
        column_info: Dict[str, Any]
    ) -> Tuple[str, List[str]]:
        """
        生成分析摘要和关键洞察
        """
        if not self.enabled:
            # 如果没有API key，返回基础摘要
            summary = f"数据包含 {statistics['shape']['rows']} 行和 {statistics['shape']['columns']} 列。"
            insights = [
                "数据已成功加载和分析",
                "请查看上方的可视化图表了解详细信息",
                "您可以使用预测功能进行进一步分析"
            ]
            return summary, insights
        
        prompt = f"""
        基于以下数据分析结果，生成一个简洁的中文摘要和3-5个关键洞察。
        
        数据描述：{data_description}
        用户需求：{user_query}
        
        统计信息：
        {json.dumps(statistics, ensure_ascii=False, indent=2)}
        
        列信息：
        {json.dumps(column_info, ensure_ascii=False, indent=2)}
        
        返回JSON格式：
        {{
            "summary": "一段简洁的摘要（2-3句话）",
            "insights": ["洞察1", "洞察2", "洞察3"]
        }}
        
        只返回JSON，不要其他文字。洞察应该是具体的、有价值的发现。
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的数据分析师，善于从数据中发现洞察。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            return result["summary"], result["insights"]
        except Exception as e:
            # 如果AI调用失败，返回基础摘要
            summary = f"数据包含 {statistics['shape']['rows']} 行和 {statistics['shape']['columns']} 列。已完成基础统计分析。"
            insights = [
                "数据质量良好，可进行进一步分析",
                "建议关注数值变量之间的相关性",
                "可以使用预测功能进行时间序列分析"
            ]
            return summary, insights
    
    async def generate_prediction_config(
        self,
        prediction_query: str,
        target_column: str,
        column_names: List[str],
        data_types: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        根据用户预测需求生成预测配置
        """
        if not self.enabled:
            return {
                "model_type": "arima",
                "forecast_periods": 10,
                "include_confidence_interval": True
            }
        
        prompt = f"""
        用户想要进行以下预测：
        
        预测需求：{prediction_query}
        目标列：{target_column}
        
        可用列：
        {json.dumps({"columns": column_names, "types": data_types}, ensure_ascii=False, indent=2)}
        
        请生成一个预测配置。返回JSON格式：
        {{
            "model_type": "arima/holtwinters/exponential_smoothing",
            "forecast_periods": 预测周期数（整数）,
            "include_confidence_interval": 是否包含置信区间（布尔值）,
            "feature_columns": 可能有用的特征列（列表，如果是时间序列预测可以为空）
        }}
        
        只返回JSON，不要其他文字。
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的数据科学家，擅长预测模型选择。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            config = json.loads(content)
            return config
        except Exception as e:
            return {
                "model_type": "arima",
                "forecast_periods": 10,
                "include_confidence_interval": True
            }

