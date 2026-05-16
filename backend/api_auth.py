import os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import (
    create_token,
    get_current_user,
    hash_password,
    validate_email,
    validate_password,
    verify_password,
)
from database import create_user, get_user_by_email, activate_vip, NORMAL_USER_USAGE_LIMIT

router = APIRouter(prefix="/api/auth", tags=["auth"])

# VIP 激活码从环境变量读取，不硬编码
VIP_ACTIVATION_CODE = os.getenv("VIP_ACTIVATION_CODE", "")


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ActivateVipRequest(BaseModel):
    code: str


def _build_user_response(user: dict) -> dict:
    is_vip = False
    vip_expire_at = None
    if user.get("is_vip") and user.get("vip_expire_at"):
        try:
            expire = datetime.fromisoformat(user["vip_expire_at"])
            if expire.tzinfo is None:
                expire = expire.replace(tzinfo=timezone.utc)
            is_vip = expire > datetime.now(timezone.utc)
            vip_expire_at = user["vip_expire_at"]
        except ValueError:
            pass

    usage_count = user.get("usage_count") or 0
    remaining = -1 if is_vip else max(0, NORMAL_USER_USAGE_LIMIT - usage_count)

    return {
        "id": user["id"],
        "email": user["email"],
        "is_vip": is_vip,
        "vip_expire_at": vip_expire_at,
        "usage_count": usage_count,
        "remaining": remaining,
    }


@router.post("/register")
async def register(req: RegisterRequest):
    if not validate_email(req.email):
        raise HTTPException(status_code=400, detail="邮箱格式不正确")

    err = validate_password(req.password)
    if err:
        raise HTTPException(status_code=400, detail=err)

    if get_user_by_email(req.email):
        raise HTTPException(status_code=400, detail="该邮箱已注册")

    hashed = hash_password(req.password)
    user = create_user(req.email, hashed)
    token = create_token(user["id"], req.email)

    # 重新获取完整用户信息
    full_user = get_user_by_email(req.email)

    return {
        "success": True,
        "data": {
            "token": token,
            "user": _build_user_response(full_user),
        },
    }


@router.post("/login")
async def login(req: LoginRequest):
    user = get_user_by_email(req.email)
    if not user:
        raise HTTPException(status_code=400, detail="邮箱或密码错误")

    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="邮箱或密码错误")

    token = create_token(user["id"], user["email"])
    return {
        "success": True,
        "data": {
            "token": token,
            "user": _build_user_response(user),
        },
    }


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "data": _build_user_response(user),
    }


@router.post("/activate-vip")
async def activate_vip_endpoint(req: ActivateVipRequest, user: dict = Depends(get_current_user)):
    """使用激活码升级为 VIP"""
    if not VIP_ACTIVATION_CODE:
        raise HTTPException(status_code=503, detail="激活码功能未配置")

    if req.code != VIP_ACTIVATION_CODE:
        raise HTTPException(status_code=400, detail="激活码错误")

    # 检查是否已经是 VIP
    if user.get("is_vip") and user.get("vip_expire_at"):
        try:
            expire = datetime.fromisoformat(user["vip_expire_at"])
            if expire.tzinfo is None:
                expire = expire.replace(tzinfo=timezone.utc)
            if expire > datetime.now(timezone.utc):
                raise HTTPException(status_code=400, detail="您已经是 VIP 会员")
        except ValueError:
            pass

    success = activate_vip(user["id"])
    if not success:
        raise HTTPException(status_code=500, detail="激活失败，请稍后重试")

    # 重新获取用户信息
    updated_user = get_user_by_email(user["email"])
    return {
        "success": True,
        "data": _build_user_response(updated_user),
    }
