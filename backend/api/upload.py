"""
数据上传API
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
import os
import uuid
from datetime import datetime
import pandas as pd
import json

from models.schemas import DatasetInfo, DataFormat, ErrorResponse

router = APIRouter()

@router.post("/dataset", response_model=DatasetInfo)
async def upload_dataset(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """
    上传数据集
    
    支持格式：CSV, JSON, TXT
    """
    try:
        # 验证文件格式
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['csv', 'json', 'txt']:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式: {file_ext}。请上传CSV、JSON或TXT文件。"
            )
        
        # 生成唯一ID
        dataset_id = str(uuid.uuid4())
        
        # 保存文件
        upload_dir = "uploads/datasets"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, f"{dataset_id}.{file_ext}")
        content = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 解析数据获取信息
        try:
            if file_ext == 'csv':
                df = pd.read_csv(file_path)
            elif file_ext == 'json':
                df = pd.read_json(file_path)
            elif file_ext == 'txt':
                # 尝试多种分隔符
                try:
                    df = pd.read_csv(file_path, sep='\t')
                except:
                    try:
                        df = pd.read_csv(file_path, sep=',')
                    except:
                        df = pd.read_csv(file_path, sep=' ')
            
            # 获取数据集信息
            rows, columns = df.shape
            column_names = df.columns.tolist()
            data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
            
        except Exception as e:
            # 清理上传的文件
            os.remove(file_path)
            raise HTTPException(
                status_code=400,
                detail=f"无法解析数据文件: {str(e)}"
            )
        
        # 保存元数据
        metadata = {
            "id": dataset_id,
            "filename": file.filename,
            "format": file_ext,
            "upload_time": datetime.now().isoformat(),
            "rows": rows,
            "columns": columns,
            "column_names": column_names,
            "data_types": data_types,
            "description": description,
            "file_path": file_path
        }
        
        metadata_path = os.path.join(upload_dir, f"{dataset_id}_metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return DatasetInfo(**metadata)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件上传失败: {str(e)}"
        )

@router.get("/dataset/{dataset_id}", response_model=DatasetInfo)
async def get_dataset_info(dataset_id: str):
    """获取数据集信息"""
    try:
        metadata_path = f"uploads/datasets/{dataset_id}_metadata.json"
        
        if not os.path.exists(metadata_path):
            raise HTTPException(
                status_code=404,
                detail="数据集不存在"
            )
        
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        return DatasetInfo(**metadata)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取数据集信息失败: {str(e)}"
        )

@router.get("/dataset/{dataset_id}/preview")
async def get_dataset_preview(dataset_id: str, rows: int = 10):
    """预览数据集前N行"""
    try:
        metadata_path = f"uploads/datasets/{dataset_id}_metadata.json"
        
        if not os.path.exists(metadata_path):
            raise HTTPException(
                status_code=404,
                detail="数据集不存在"
            )
        
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        file_path = metadata["file_path"]
        file_ext = metadata["format"]
        
        if file_ext == 'csv':
            df = pd.read_csv(file_path, nrows=rows)
        elif file_ext == 'json':
            df = pd.read_json(file_path)
            df = df.head(rows)
        elif file_ext == 'txt':
            df = pd.read_csv(file_path, sep='\t', nrows=rows)
        
        return {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": df.columns.tolist(),
            "data": df.to_dict(orient='records')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"预览数据失败: {str(e)}"
        )

