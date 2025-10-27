"""
用户管理API
"""
from fastapi import APIRouter, HTTPException
from typing import List
import json
import os
from datetime import datetime
import uuid

from models.schemas import UserInfo, WorkRecord

router = APIRouter()

# 模拟用户数据库（实际应用中应使用真实数据库）
USERS_FILE = "uploads/users.json"

def load_users():
    """加载用户数据"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    """保存用户数据"""
    os.makedirs("uploads", exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2, default=str)

@router.post("/register")
async def register_user(username: str, email: str = None):
    """
    用户注册（简化版，仅UI演示）
    """
    try:
        users = load_users()
        
        # 检查用户名是否存在
        for user_data in users.values():
            if user_data["username"] == username:
                raise HTTPException(
                    status_code=400,
                    detail="用户名已存在"
                )
        
        user_id = str(uuid.uuid4())
        user = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "work_records": []
        }
        
        users[user_id] = user
        save_users(users)
        
        return UserInfo(**user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"注册失败: {str(e)}"
        )

@router.get("/info/{user_id}", response_model=UserInfo)
async def get_user_info(user_id: str):
    """获取用户信息"""
    try:
        users = load_users()
        
        if user_id not in users:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        return UserInfo(**users[user_id])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取用户信息失败: {str(e)}"
        )

@router.get("/records/{user_id}", response_model=List[WorkRecord])
async def get_work_records(user_id: str):
    """获取用户的工作记录"""
    try:
        users = load_users()
        
        if user_id not in users:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        records = users[user_id].get("work_records", [])
        return [WorkRecord(**record) for record in records]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取工作记录失败: {str(e)}"
        )

@router.post("/records/{user_id}")
async def add_work_record(user_id: str, record: WorkRecord):
    """添加工作记录"""
    try:
        users = load_users()
        
        if user_id not in users:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        record_dict = record.model_dump(mode='json')
        record_dict["created_at"] = datetime.now().isoformat()
        record_dict["updated_at"] = datetime.now().isoformat()
        
        users[user_id]["work_records"].append(record_dict)
        save_users(users)
        
        return {"message": "工作记录添加成功", "record": record_dict}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"添加工作记录失败: {str(e)}"
        )

@router.delete("/records/{user_id}/{record_id}")
async def delete_work_record(user_id: str, record_id: str):
    """删除工作记录"""
    try:
        users = load_users()
        
        if user_id not in users:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        records = users[user_id]["work_records"]
        updated_records = [r for r in records if r["record_id"] != record_id]
        
        if len(updated_records) == len(records):
            raise HTTPException(
                status_code=404,
                detail="工作记录不存在"
            )
        
        users[user_id]["work_records"] = updated_records
        save_users(users)
        
        return {"message": "工作记录删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除工作记录失败: {str(e)}"
        )

